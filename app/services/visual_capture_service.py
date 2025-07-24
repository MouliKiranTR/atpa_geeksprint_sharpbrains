"""
Visual Capture Service for taking screenshots of Figma files and Lucid diagrams

This service provides both base64 screenshot capture and file export 
capabilities for integration with various analysis workflows.
"""

import base64
import asyncio
import time
import os
import tempfile
from typing import Dict, Any, Optional, List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import httpx

from app.core.config import settings
from app.services.cache_service import cache_service


class VisualCaptureService:
    """Service for capturing visual content from web sources"""
    
    def __init__(self):
        self.figma_token = settings.FIGMA_API_TOKEN
        self.lucid_api_key = settings.LUCID_API_KEY
        self.temp_dir = None
        self._ensure_temp_directory()
    
    def _ensure_temp_directory(self):
        """Create temporary directory for file exports"""
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            self.temp_dir = tempfile.mkdtemp(prefix="visual_capture_")
    
    def get_temp_directory(self) -> str:
        """Get the temporary directory path"""
        return self.temp_dir
    
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
        file_name: str = "Figma File",
        export_to_file: bool = False
    ) -> Dict[str, Any]:
        """
        Capture screenshot of a Figma file
        
        Args:
            file_key: Figma file key
            file_name: Name of the file for context
            export_to_file: Whether to export to temporary file
            
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
                result = {
                    "success": True,
                    "file_key": file_key,
                    "file_name": file_name,
                    "screenshot_base64": screenshot_data,
                    "metadata": file_metadata,
                    "source": "figma",
                    "capture_method": "api"
                }
                
                # Export to file if requested
                if export_to_file:
                    file_path = await self._save_base64_to_file(
                        screenshot_data, file_key, file_name, "figma"
                    )
                    if file_path:
                        result["file_path"] = file_path
                
                return result
            else:
                # Fallback to web screenshot
                return await self._capture_figma_web_screenshot(
                    file_key, file_name, export_to_file
                )
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to capture Figma screenshot: {str(e)}"
            }

    async def _get_figma_file_metadata(
        self, file_key: str
    ) -> Dict[str, Any]:
        """
        Get metadata for a Figma file
        
        Args:
            file_key: Figma file key
            
        Returns:
            File metadata dictionary
        """
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    'X-FIGMA-TOKEN': self.figma_token
                }
                
                response = await client.get(
                    f"https://api.figma.com/v1/files/{file_key}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "name": data.get("name", "Unknown"),
                        "version": data.get("version", "Unknown"),
                        "last_modified": data.get("lastModified", "Unknown"),
                        "thumbnail_url": data.get("thumbnailUrl", "")
                    }
                else:
                    msg = (
                        f"⚠️ Failed to get Figma metadata: "
                        f"{response.status_code}"
                    )
                    print(msg)
                    return {}
                    
        except Exception as e:
            print(f"⚠️ Error getting Figma metadata: {e}")
            return {}

    async def _get_figma_screenshot_api(self, file_key: str) -> Optional[str]:
        """
        Get screenshot using Figma's image export API
        
        Args:
            file_key: Figma file key
            
        Returns:
            Base64 encoded screenshot or None if failed
        """
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    'X-FIGMA-TOKEN': self.figma_token
                }
                
                # Get image URLs
                params = {
                    'ids': file_key,
                    'format': 'png',
                    'scale': 2
                }
                
                response = await client.get(
                    f"https://api.figma.com/v1/images/{file_key}",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    image_urls = data.get('images', {})
                    
                    if image_urls:
                        # Get the first image URL
                        image_url = list(image_urls.values())[0]
                        
                        # Download the image
                        img_response = await client.get(image_url)
                        if img_response.status_code == 200:
                            return base64.b64encode(
                                img_response.content
                            ).decode('utf-8')
                
                return None
                
        except Exception as e:
            print(f"⚠️ Figma API screenshot failed: {e}")
            return None

    async def _capture_figma_web_screenshot(
        self, 
        file_key: str, 
        file_name: str,
        export_to_file: bool = False
    ) -> Dict[str, Any]:
        """
        Capture Figma file screenshot using web automation
        
        Args:
            file_key: Figma file key
            file_name: Name of the file
            export_to_file: Whether to export to file
            
        Returns:
            Screenshot result dictionary
        """
        try:
            chrome_options = self._get_chrome_options()
            driver = webdriver.Chrome(options=chrome_options)
            
            try:
                # Navigate to Figma file
                figma_url = f"https://www.figma.com/file/{file_key}"
                driver.get(figma_url)
                
                # Wait for page to load
                time.sleep(5)
                
                # Take screenshot
                screenshot_data = driver.get_screenshot_as_base64()
                
                result = {
                    "success": True,
                    "file_key": file_key,
                    "file_name": file_name,
                    "screenshot_base64": screenshot_data,
                    "metadata": {"capture_method": "web_automation"},
                    "source": "figma",
                    "capture_method": "web"
                }
                
                # Export to file if requested
                if export_to_file:
                    file_path = await self._save_base64_to_file(
                        screenshot_data, file_key, file_name, "figma"
                    )
                    if file_path:
                        result["file_path"] = file_path
                
                return result
                
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
        diagram_title: str = "Lucid Diagram",
        use_cache: bool = True,
        format: str = "png",
        export_to_file: bool = False
    ) -> Dict[str, Any]:
        """
        Capture screenshot of a Lucid diagram with caching support
        
        Args:
            diagram_id: Lucid diagram ID
            diagram_title: Title of the diagram for context
            use_cache: Whether to use caching (default: True)
            format: Export format (default: png)
            export_to_file: Whether to export to temporary file
            
        Returns:
            Dictionary with screenshot data and metadata
        """
        if not self.lucid_api_key:
            return {
                "success": False,
                "error": "Lucid API key not configured"
            }
        
        try:
            # Check cache first if enabled
            if use_cache:
                cached_result = await cache_service.get_cached_export(
                    diagram_id, format
                )
                if cached_result:
                    # Convert cached result to expected format
                    result = {
                        "success": True,
                        "diagram_id": diagram_id,
                        "diagram_title": diagram_title,
                        "screenshot_base64": base64.b64encode(
                            cached_result["image_data"]
                        ).decode('utf-8'),
                        "metadata": cached_result.get("metadata", {}),
                        "source": "lucid",
                        "capture_method": "cached",
                        "file_path": cached_result.get("file_path")
                    }
                    
                    # Export to file if requested and not already cached as file
                    if export_to_file and not result.get("file_path"):
                        file_path = await self._save_base64_to_file(
                            result["screenshot_base64"], 
                            diagram_id, 
                            diagram_title, 
                            "lucid"
                        )
                        if file_path:
                            result["file_path"] = file_path
                    
                    return result
            
            # Try to use Lucid service for export
            from app.services.lucid_service import lucid_service
            if lucid_service:
                export_result = await lucid_service.export_document_image(
                    document_id=diagram_id,
                    format=format,
                    use_cache=use_cache
                )
                
                if export_result.get("success"):
                    result = {
                        "success": True,
                        "diagram_id": diagram_id,
                        "diagram_title": diagram_title,
                        "screenshot_base64": base64.b64encode(
                            export_result["image_data"]
                        ).decode('utf-8'),
                        "metadata": export_result.get("metadata", {}),
                        "source": "lucid",
                        "capture_method": "lucid_service",
                        "file_path": export_result.get("file_path")
                    }
                    
                    # Export to file if requested and not already available
                    if export_to_file and not result.get("file_path"):
                        file_path = await self._save_base64_to_file(
                            result["screenshot_base64"], 
                            diagram_id, 
                            diagram_title, 
                            "lucid"
                        )
                        if file_path:
                            result["file_path"] = file_path
                    
                    return result
            
            # Legacy fallback methods...
            # Try to get export URL from Lucid API
            export_data = await self._get_lucid_export_url(diagram_id)
            
            if export_data:
                # Download the exported image
                image_data = await self._download_lucid_export(
                    export_data["url"]
                )
                
                if image_data:
                    result = {
                        "success": True,
                        "diagram_id": diagram_id,
                        "diagram_title": diagram_title,
                        "screenshot_base64": image_data,
                        "metadata": {"export_format": format},
                        "source": "lucid",
                        "capture_method": "api_export"
                    }
                    
                    # Export to file if requested
                    if export_to_file:
                        file_path = await self._save_base64_to_file(
                            image_data, diagram_id, diagram_title, "lucid"
                        )
                        if file_path:
                            result["file_path"] = file_path
                    
                    return result
            
            # Final fallback: web screenshot
            return await self._capture_lucid_web_screenshot(
                diagram_id, diagram_title, export_to_file
            )
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to capture Lucid screenshot: {str(e)}"
            }

    async def _get_lucid_export_url(
        self, 
        diagram_id: str, 
        format: str = "png"
    ) -> Optional[Dict[str, Any]]:
        """Get export URL for Lucid diagram"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.lucid_api_key}",
                    "Lucid-Api-Version": "1"
                }
                
                export_data = {
                    "format": format,
                    "size": "large"
                }
                
                url = f"https://api.lucid.co/documents/{diagram_id}/export"
                response = await client.post(
                    url, headers=headers, json=export_data
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    msg = (
                        f"⚠️ Lucid export API error: "
                        f"{response.status_code}"
                    )
                    print(msg)
                    return None
                    
        except Exception as e:
            print(f"⚠️ Error getting Lucid export URL: {e}")
            return None

    async def _download_lucid_export(self, export_url: str) -> Optional[str]:
        """Download exported Lucid diagram"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(export_url)
                
                if response.status_code == 200:
                    return base64.b64encode(
                        response.content
                    ).decode('utf-8')
                else:
                    return None
                    
        except Exception as e:
            print(f"⚠️ Error downloading Lucid export: {e}")
            return None

    async def _capture_lucid_web_screenshot(
        self, 
        diagram_id: str, 
        diagram_title: str,
        export_to_file: bool = False
    ) -> Dict[str, Any]:
        """Capture Lucid diagram using web automation"""
        try:
            chrome_options = self._get_chrome_options()
            driver = webdriver.Chrome(options=chrome_options)
            
            try:
                # Navigate to Lucid diagram
                lucid_url = f"https://lucid.app/documents/view/{diagram_id}"
                driver.get(lucid_url)
                
                # Wait for page to load
                time.sleep(10)
                
                # Take screenshot
                screenshot_data = driver.get_screenshot_as_base64()
                
                result = {
                    "success": True,
                    "diagram_id": diagram_id,
                    "diagram_title": diagram_title,
                    "screenshot_base64": screenshot_data,
                    "metadata": {"capture_method": "web_automation"},
                    "source": "lucid",
                    "capture_method": "web"
                }
                
                # Export to file if requested
                if export_to_file:
                    file_path = await self._save_base64_to_file(
                        screenshot_data, diagram_id, diagram_title, "lucid"
                    )
                    if file_path:
                        result["file_path"] = file_path
                
                return result
                
            finally:
                driver.quit()
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Web screenshot failed: {str(e)}"
            }
    
    async def capture_multiple_screenshots(
        self, 
        items: List[Dict[str, Any]],
        export_to_files: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Capture screenshots for multiple items in parallel
        
        Args:
            items: List of items with 'type', 'id', and 'name' fields
            export_to_files: Whether to export screenshots to files
            
        Returns:
            List of screenshot results
        """
        if not items:
            return []
        
        print(f"📷 Starting parallel capture for {len(items)} items...")
        
        # Create capture tasks for parallel execution
        capture_tasks = []
        
        for item in items:
            if item.get("type") == "figma":
                task = self.capture_figma_file_screenshot(
                    item.get("id", ""), 
                    item.get("name", "Figma File"),
                    export_to_file=export_to_files
                )
            elif item.get("type") == "lucid":
                task = self.capture_lucid_diagram_screenshot(
                    item.get("id", ""), 
                    item.get("name", "Lucid Diagram"),
                    export_to_file=export_to_files
                )
            else:
                # Create a coroutine that returns an error result
                async def create_error_result():
                    return {
                        "success": False,
                        "error": (
                            f"Unsupported item type: {item.get('type')}"
                        )
                    }
                task = create_error_result()
            
            capture_tasks.append(task)
        
        # Execute all captures in parallel
        parallel_msg = f"⚡ Executing {len(capture_tasks)} capture tasks"
        print(f"{parallel_msg} in parallel...")
        start_time = time.time()
        
        try:
            # Use asyncio.gather to execute all tasks concurrently
            results = await asyncio.gather(
                *capture_tasks, return_exceptions=True
            )
            
            # Process results and handle any exceptions
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    error_msg = f"⚠️ Capture task {i} failed with exception:"
                    print(f"{error_msg} {result}")
                    processed_results.append({
                        "success": False,
                        "error": f"Capture failed: {str(result)}"
                    })
                else:
                    processed_results.append(result)
            
            processing_time = time.time() - start_time
            print(f"✅ Parallel capture completed in {processing_time:.2f}s")
            
            success_count = sum(
                1 for r in processed_results if r.get('success')
            )
            total_count = len(processed_results)
            print(f"📊 Success rate: {success_count} / {total_count}")
            
            return processed_results
            
        except Exception as e:
            print(f"🚨 Parallel capture failed: {e}")
            # Return error results for all items
            return [
                {
                    "success": False,
                    "error": f"Parallel capture error: {str(e)}"
                }
                for _ in items
            ]
    
    async def _save_base64_to_file(
        self,
        base64_data: str,
        item_id: str,
        item_title: str,
        source: str
    ) -> Optional[str]:
        """
        Convert base64 screenshot data to temporary file
        
        Args:
            base64_data: Base64 encoded image data
            item_id: ID of the item (diagram_id, file_key, etc.)
            item_title: Title/name of the item
            source: Source type (lucid, figma, etc.)
            
        Returns:
            Path to temporary file or None if failed
        """
        try:
            # Decode base64 data
            image_data = base64.b64decode(base64_data)
            
            # Create safe filename
            allowed_chars = (' ', '-', '_')
            safe_title = "".join(
                c for c in item_title 
                if c.isalnum() or c in allowed_chars
            ).rstrip()
            safe_title = safe_title.replace(' ', '_')
            
            filename = f"{source}_{item_id}_{safe_title}_screenshot.png"
            file_path = os.path.join(self.temp_dir, filename)
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            print(f"✅ Saved {source} screenshot to: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"Error saving {source} screenshot to file: {e}")
            return None
    
    def cleanup_temp_files(self, file_paths: List[str]) -> None:
        """Clean up specific temporary files"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"🗑️  Cleaned up: {file_path}")
            except Exception as e:
                print(f"⚠️ Failed to clean up {file_path}: {e}")
    
    def cleanup_temp_directory(self) -> None:
        """Clean up entire temporary directory"""
        try:
            if self.temp_dir and os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir)
                print(f"🗑️  Cleaned up temp directory: {self.temp_dir}")
                self.temp_dir = None
        except Exception as e:
            print(f"⚠️ Failed to clean up temp directory: {e}")


# Create service instance
visual_capture_service = VisualCaptureService() 