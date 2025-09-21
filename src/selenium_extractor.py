"""
Selenium 기반 Instagram 게시물 텍스트 추출 모듈
"""

import re
import time
import random
from typing import Dict, List, Optional
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    WebDriverException,
    StaleElementReferenceException
)
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


@dataclass
class ExtractResult:
    """추출 결과 데이터 클래스"""
    title: str
    url: str
    text: str
    username: str
    success: bool
    error_message: str = ""
    extraction_time: str = ""


class SeleniumInstagramExtractor:
    """Selenium 기반 Instagram 게시물 텍스트 추출기"""
    
    def __init__(self, headless: bool = True, max_workers: int = 5):
        """
        초기화
        
        Args:
            headless (bool): 헤드리스 모드 사용 여부
            max_workers (int): 최대 스레드 수
        """
        self.headless = headless
        self.max_workers = max_workers
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
    def _create_driver(self) -> webdriver.Chrome:
        """Chrome WebDriver 인스턴스 생성"""
        try:
            options = Options()
            
            if self.headless:
                options.add_argument("--headless")
            
            # 반감지 및 성능 최적화 옵션
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")
            options.add_argument("--disable-javascript")  # JavaScript 비활성화로 빠른 로딩
            
            # 랜덤 User-Agent 설정
            user_agent = random.choice(self.user_agents)
            options.add_argument(f"--user-agent={user_agent}")
            
            # ChromeDriver 서비스 설정
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            # 스크립트 감지 방지
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # 암묵적 대기 설정
            driver.implicitly_wait(10)
            
            return driver
            
        except Exception as e:
            raise RuntimeError(f"ChromeDriver 생성 실패: {str(e)}")
    
    def validate_url(self, url: str) -> bool:
        """Instagram URL 유효성 검증"""
        try:
            parsed_url = urlparse(url)
            
            if parsed_url.netloc not in ["www.instagram.com", "instagram.com"]:
                return False
                
            path_pattern = r"^/(p|reel|tv)/([A-Za-z0-9_-]+)/?"
            if not re.match(path_pattern, parsed_url.path):
                return False
                
            return True
        except Exception:
            return False
    
    def _extract_text_from_page(self, driver: webdriver.Chrome, url: str) -> Dict[str, str]:
        """페이지에서 텍스트 및 메타데이터 추출"""
        try:
            # 페이지 로드
            driver.get(url)
            
            # 페이지 로딩 대기 (최대 15초)
            wait = WebDriverWait(driver, 15)
            
            # 여러 가능한 셀렉터 시도
            caption_selectors = [
                "meta[property='og:description']",
                "meta[name='description']",
                "[data-testid='post-caption']", 
                "article h1",
                ".x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj",
                "span._aacl._aaco._aacu._aacx._aad7._aade",
                "div._a9zs"
            ]
            
            username = "알 수 없음"
            caption_text = ""
            
            # 사용자명 추출
            try:
                username_selectors = [
                    "a[href*='/'][role='link'] span",
                    "header a span",
                    ".x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.xtrsf7v.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.x1rod4b6.xo1l8bm.x10wh9bi.x1wdrske.x8viiok.x18hxmgj"
                ]
                
                for selector in username_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            text = element.text.strip()
                            if text and not text.startswith('@') and len(text) > 0:
                                username = text
                                break
                        if username != "알 수 없음":
                            break
                    except:
                        continue
                        
            except Exception:
                pass
            
            # 캡션 텍스트 추출
            for selector in caption_selectors:
                try:
                    if selector.startswith("meta"):
                        # 메타 태그에서 추출
                        element = driver.find_element(By.CSS_SELECTOR, selector)
                        content = element.get_attribute("content")
                        if content and len(content.strip()) > 10:
                            caption_text = content.strip()
                            break
                    else:
                        # 일반 요소에서 추출
                        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        text = element.text.strip()
                        if text and len(text) > 10:
                            caption_text = text
                            break
                except:
                    continue
            
            # BeautifulSoup로 추가 파싱 시도
            if not caption_text:
                try:
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    # og:description 메타 태그
                    meta_desc = soup.find('meta', property='og:description')
                    if meta_desc and meta_desc.get('content'):
                        caption_text = meta_desc['content'].strip()
                    
                    # 일반 description 메타 태그
                    if not caption_text:
                        meta_desc = soup.find('meta', attrs={'name': 'description'})
                        if meta_desc and meta_desc.get('content'):
                            caption_text = meta_desc['content'].strip()
                            
                except Exception:
                    pass
            
            # 텍스트가 없으면 비디오 컨텐츠로 처리
            if not caption_text or len(caption_text.strip()) < 5:
                caption_text = "동영상콘텐츠"
            
            return {
                "username": username,
                "text": self._clean_text(caption_text)
            }
            
        except TimeoutException:
            return {"username": "알 수 없음", "text": "동영상콘텐츠"}
        except Exception as e:
            raise RuntimeError(f"텍스트 추출 실패: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """텍스트 정제"""
        if not text:
            return "동영상콘텐츠"
            
        # 불필요한 공백 및 특수문자 정제
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Instagram 관련 불필요한 텍스트 제거
        unwanted_patterns = [
            r'Instagram에서 이 게시물 보기',
            r'shared a post on Instagram',
            r'팔로우',
            r'likes',
            r'followers',
            r'following',
            r'Follow',
            r'Posted by'
        ]
        
        for pattern in unwanted_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        text = text.strip()
        
        if len(text) < 5:
            return "동영상콘텐츠"
            
        return text
    
    def extract_single_url(self, url: str, title: str = "미정") -> ExtractResult:
        """단일 URL에서 텍스트 추출"""
        driver = None
        try:
            if not self.validate_url(url):
                return ExtractResult(
                    title=title,
                    url=url,
                    text="",
                    username="",
                    success=False,
                    error_message="유효하지 않은 Instagram URL"
                )
            
            driver = self._create_driver()
            
            # 랜덤 대기 (1-3초)
            time.sleep(random.uniform(1, 3))
            
            result = self._extract_text_from_page(driver, url)
            
            return ExtractResult(
                title=title,
                url=url,
                text=result["text"],
                username=result["username"],
                success=True,
                extraction_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
        except Exception as e:
            return ExtractResult(
                title=title,
                url=url,
                text="",
                username="",
                success=False,
                error_message=str(e)
            )
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def batch_extract(self, url_data: List[tuple]) -> List[ExtractResult]:
        """
        배치 처리로 여러 URL에서 텍스트 추출
        
        Args:
            url_data: (title, url) 튜플의 리스트
            
        Returns:
            List[ExtractResult]: 추출 결과 리스트
        """
        results = []
        
        print(f"🚀 {len(url_data)}개 URL 배치 처리 시작 (최대 {self.max_workers}개 스레드)")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 모든 작업 제출
            future_to_data = {
                executor.submit(self.extract_single_url, url, title): (title, url)
                for title, url in url_data
            }
            
            # 완료된 작업 처리
            for i, future in enumerate(as_completed(future_to_data), 1):
                title, url = future_to_data[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    status = "✅ 성공" if result.success else f"❌ 실패: {result.error_message}"
                    print(f"  [{i}/{len(url_data)}] {title[:30]}... - {status}")
                    
                except Exception as e:
                    # 예외 발생 시 실패 결과 생성
                    result = ExtractResult(
                        title=title,
                        url=url,
                        text="",
                        username="",
                        success=False,
                        error_message=f"처리 중 예외 발생: {str(e)}"
                    )
                    results.append(result)
                    print(f"  [{i}/{len(url_data)}] {title[:30]}... - ❌ 예외: {str(e)}")
        
        # 성공/실패 통계 출력
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        print(f"\n📊 배치 처리 완료: 성공 {successful}개, 실패 {failed}개")
        
        return results