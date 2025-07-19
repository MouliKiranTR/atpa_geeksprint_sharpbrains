"""
Visual Capture Service for taking screenshots of Figma files and Lucid diagrams
"""

import base64
import asyncio
import time
from typing import Dict, Any, Optional, List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import httpx

from app.core.config import settings


class VisualCaptureService:
    """Service for capturing visual content from web sources"""
    
    def __init__(self):
        self.figma_token = settings.FIGMA_API_TOKEN
        self.lucid_api_key = settings.LUCID_API_KEY
    
    def _get_chrome_options(self) -> Options:
        """Get Chrome options for headless browsing"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        return chrome_options
    
    async def capture_figma_file_screenshot(
        self, 
        file_key: str, 
        file_name: str = "Figma File"
    ) -> Dict[str, Any]:
        """
        Capture screenshot of a Figma file
        
        Args:
            file_key: Figma file key
            file_name: Name of the file for context
            
        Returns:
            Dictionary with screenshot data and metadata
        """
        if not self.figma_token:
            return {
                "success": False,
                "error": "Figma API token not configured"
            }
        
        try:
            # First try to get file metadata
            file_metadata = await self._get_figma_file_metadata(file_key)
            
            # Get screenshot using Figma's API
            screenshot_data = await self._get_figma_screenshot_api(file_key)
            
            if screenshot_data:
                return {
                    "success": True,
                    "file_key": file_key,
                    "file_name": file_name,
                    "screenshot_base64": screenshot_data,
                    "metadata": file_metadata,
                    "source": "figma",
                    "capture_method": "api"
                }
            else:
                # Fallback to web screenshot
                return await self._capture_figma_web_screenshot(
                    file_key, file_name
                )
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to capture Figma screenshot: {str(e)}"
            }
    
    async def _get_figma_file_metadata(self, file_key: str) -> Dict[str, Any]:
        """Get additional metadata about a Figma file"""
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(
                    f"https://api.figma.com/v1/files/{file_key}",
                    headers={"X-Figma-Token": self.figma_token},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    document_children = data.get("document", {}).get(
                        "children", []
                    )
                    return {
                        "document_name": data.get("name", ""),
                        "last_modified": data.get("lastModified", ""),
                        "version": data.get("version", ""),
                        "pages": len(document_children),
                        "description": data.get("description", "")
                    }
        except Exception as e:
            print(f"Error getting Figma metadata: {e}")
        
        return {}
    
    async def _get_figma_screenshot_api(self, file_key: str) -> Optional[str]:
        """Get screenshot using Figma's image API"""
        try:
            # Get image URL from Figma API
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(
                    f"https://api.figma.com/v1/images/{file_key}",
                    headers={"X-Figma-Token": self.figma_token},
                    params={
                        "format": "png",
                        "scale": 2
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    image_url = data.get("images", {}).get(file_key)
                    
                    if image_url:
                        # Download the image
                        img_response = await client.get(
                            image_url, timeout=30.0
                        )
                        if img_response.status_code == 200:
                            return base64.b64encode(
                                img_response.content
                            ).decode('utf-8')
        
        except Exception as e:
            print(f"Error getting Figma screenshot via API: {e}")
        
        return None
    
    async def _capture_figma_web_screenshot(
        self, 
        file_key: str, 
        file_name: str
    ) -> Dict[str, Any]:
        """Fallback web screenshot capture for Figma"""
        try:
            figma_url = f"https://www.figma.com/file/{file_key}"
            
            driver = webdriver.Chrome(options=self._get_chrome_options())
            
            try:
                driver.get(figma_url)
                time.sleep(5)  # Wait for content to load
                
                # Take screenshot
                screenshot = driver.get_screenshot_as_png()
                screenshot_base64 = base64.b64encode(screenshot).decode('utf-8')
                
                return {
                    "success": True,
                    "file_key": file_key,
                    "file_name": file_name,
                    "screenshot_base64": screenshot_base64,
                    "metadata": {},
                    "source": "figma",
                    "capture_method": "web_screenshot"
                }
                
            finally:
                driver.quit()
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Web screenshot failed: {str(e)}"
            }
    
    async def capture_lucid_diagram_screenshot(
        self, 
        diagram_id: str, 
        diagram_title: str = "Lucid Diagram"
    ) -> Dict[str, Any]:
        """
        Capture screenshot of a Lucid diagram
        
        Args:
            diagram_id: Lucid diagram ID
            diagram_title: Title of the diagram for context
            
        Returns:
            Dictionary with screenshot data and metadata
        """
        if not self.lucid_api_key:
            return {
                "success": False,
                "error": "Lucid API key not configured"
            }
        
        try:
            # Try to get export URL from Lucid API
            export_data = await self._get_lucid_export_url(diagram_id)
            
            if export_data and export_data.get("export_url"):
                # Download the exported image
                screenshot_data = await self._download_lucid_export(
                    export_data["export_url"]
                )
                
                if screenshot_data:
                    return {
                        "success": True,
                        "diagram_id": diagram_id,
                        "diagram_title": diagram_title,
                        "screenshot_base64": screenshot_data,
                        "metadata": export_data.get("metadata", {}),
                        "source": "lucid",
                        "capture_method": "api_export"
                    }
            
            # Fallback to web screenshot
            return await self._capture_lucid_web_screenshot(
                diagram_id, diagram_title
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to capture Lucid screenshot: {str(e)}"
            }
    
    async def _get_lucid_export_url(
        self, diagram_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get export URL for Lucid diagram"""
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.post(
                    f"https://api.lucid.co/documents/{diagram_id}/export",
                    headers={
                        "Authorization": f"Bearer {self.lucid_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "format": "PNG",
                        "pageSelection": "ALL",
                        "scale": 2
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "export_url": data.get("url"),
                        "metadata": {
                            "export_id": data.get("id"),
                            "format": "PNG",
                            "scale": 2
                        }
                    }
        
        except Exception as e:
            print(f"Error getting Lucid export URL: {e}")
        
        return None
    
    async def _download_lucid_export(self, export_url: str) -> Optional[str]:
        """Download exported Lucid diagram image"""
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(export_url, timeout=60.0)
                
                if response.status_code == 200:
                    return base64.b64encode(response.content).decode('utf-8')
        
        except Exception as e:
            print(f"Error downloading Lucid export: {e}")
        
        return None
    
    async def _capture_lucid_web_screenshot(
        self, 
        diagram_id: str, 
        diagram_title: str
    ) -> Dict[str, Any]:
        """Fallback web screenshot capture for Lucid"""
        try:
            # Construct Lucid URL 
            lucid_url = f"https://lucid.app/lucidchart/{diagram_id}/view"
            
            driver = webdriver.Chrome(options=self._get_chrome_options())
            
            try:
                driver.get(lucid_url)
                time.sleep(8)  # Wait longer for Lucid to load
                
                # Try to wait for diagram content
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "canvas"))
                    )
                except Exception:
                    pass  # Continue even if canvas not found
                
                # Take screenshot
                screenshot = driver.get_screenshot_as_png()
                screenshot_base64 = base64.b64encode(screenshot).decode('utf-8')
                
                return {
                    "success": True,
                    "diagram_id": diagram_id,
                    "diagram_title": diagram_title,
                    "screenshot_base64": screenshot_base64,
                    "metadata": {},
                    "source": "lucid",
                    "capture_method": "web_screenshot"
                }
                
            finally:
                driver.quit()
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Web screenshot failed: {str(e)}"
            }
    
    async def capture_multiple_screenshots(
        self, 
        items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Capture screenshots for multiple items
        
        Args:
            items: List of items with 'type', 'id', and 'name' fields
            
        Returns:
            List of screenshot results
        """
        results = []
        
        for item in items:
            if item.get("type") == "figma":
                result = await self.capture_figma_file_screenshot(
                    item.get("id", ""), 
                    item.get("name", "Figma File")
                )
            elif item.get("type") == "lucid":
                result = await self.capture_lucid_diagram_screenshot(
                    item.get("id", ""), 
                    item.get("name", "Lucid Diagram")
                )
            else:
                result = {
                    "success": False,
                    "error": f"Unsupported item type: {item.get('type')}"
                }
            
            results.append(result)
            
            # Add small delay between captures to be respectful
            await asyncio.sleep(1)
        
        return results


# Create service instance
visual_capture_service = VisualCaptureService() 