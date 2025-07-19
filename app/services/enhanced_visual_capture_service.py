"""
Enhanced Visual Capture Service with temporary file export for OpenArena
"""

import os
import tempfile
import asyncio
import httpx
from typing import Dict, Any, List, Optional

from app.core.config import settings


class EnhancedVisualCaptureService:
    """Enhanced service for capturing visual content with file export"""
    
    def __init__(self):
        self.figma_token = settings.FIGMA_API_TOKEN
        self.lucid_api_key = settings.LUCID_API_KEY
        self.temp_dir = None
        self._ensure_temp_directory()
    
    def _ensure_temp_directory(self):
        """Create temporary directory for exports"""
        if not self.temp_dir or not os.path.exists(self.temp_dir):
            self.temp_dir = tempfile.mkdtemp(prefix="visual_capture_")
            
    def get_temp_directory(self) -> str:
        """Get the temporary directory path"""
        return self.temp_dir
    
    async def capture_and_export_lucid_diagram(
        self, 
        diagram_id: str, 
        diagram_title: str = "Lucid Diagram"
    ) -> Dict[str, Any]:
        """
        Capture Lucid diagram and export to temporary file
        
        Args:
            diagram_id: Lucid diagram ID
            diagram_title: Title of the diagram for context
            
        Returns:
            Dictionary with export data and file path
        """
        if not self.lucid_api_key:
            return {
                "success": False,
                "error": "Lucid API key not configured"
            }
        
        try:
            # Try API export first
            export_data = await self._create_lucid_export(diagram_id)
            
            if export_data and export_data.get("image_data"):
                # API export successful - save to file
                file_path = await self._download_and_save_lucid_export(
                    export_data["image_data"], 
                    diagram_id,
                    diagram_title
                )
                
                if file_path:
                    return {
                        "success": True,
                        "diagram_id": diagram_id,
                        "diagram_title": diagram_title,
                        "file_path": file_path,
                        "metadata": export_data.get("metadata", {}),
                        "source": "lucid",
                        "capture_method": "api_export_file"
                    }
            
            # API export failed - fall back to screenshot method
            print("🔄 Lucid API export failed, falling back to screenshot capture...")
            
            # Import and use the old visual capture service as fallback
            from app.services.visual_capture_service import VisualCaptureService
            fallback_service = VisualCaptureService()
            
            screenshot_result = await fallback_service.capture_lucid_diagram_screenshot(
                diagram_id, diagram_title
            )
            
            if screenshot_result.get("success") and screenshot_result.get("screenshot_base64"):
                # Convert base64 screenshot to temporary file
                file_path = await self._save_base64_to_file(
                    screenshot_result["screenshot_base64"],
                    diagram_id,
                    diagram_title,
                    "lucid"
                )
                
                if file_path:
                    return {
                        "success": True,
                        "diagram_id": diagram_id,
                        "diagram_title": diagram_title,
                        "file_path": file_path,
                        "metadata": screenshot_result.get("metadata", {}),
                        "source": "lucid",
                        "capture_method": "fallback_screenshot_file"
                    }
            
            return {
                "success": False,
                "error": "All Lucid capture methods failed"
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to capture Lucid diagram: {str(e)}"
            }
    
    async def capture_and_export_figma_file(
        self, 
        file_key: str, 
        file_name: str = "Figma File"
    ) -> Dict[str, Any]:
        """
        Capture Figma file and export to temporary file
        
        Args:
            file_key: Figma file key
            file_name: Name of the file for context
            
        Returns:
            Dictionary with export data and file path
        """
        if not self.figma_token:
            return {
                "success": False,
                "error": "Figma API token not configured"
            }
        
        try:
            # Get Figma image using API
            image_data = await self._get_figma_image_data(file_key)
            
            if not image_data:
                return {
                    "success": False,
                    "error": "Failed to get Figma image data"
                }
            
            # Save to temporary file
            file_path = await self._save_figma_image_to_file(
                image_data, 
                file_key, 
                file_name
            )
            
            if file_path:
                # Get file metadata
                file_metadata = await self._get_figma_file_metadata(file_key)
                
                return {
                    "success": True,
                    "file_key": file_key,
                    "file_name": file_name,
                    "file_path": file_path,
                    "metadata": file_metadata,
                    "source": "figma",
                    "capture_method": "api_export_file"
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to save Figma image to file"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to capture Figma file: {str(e)}"
            }
    
    async def capture_multiple_to_files(
        self, 
        items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Capture multiple items and export to files
        
        Args:
            items: List of items with 'type', 'id', and 'name' fields
            
        Returns:
            List of capture results with file paths
        """
        results = []
        
        for item in items:
            if item.get("type") == "figma":
                result = await self.capture_and_export_figma_file(
                    item.get("id", ""), 
                    item.get("name", "Figma File")
                )
            elif item.get("type") == "lucid":
                result = await self.capture_and_export_lucid_diagram(
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
    
    async def _create_lucid_export(
        self, diagram_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get Lucid diagram image using multiple approaches"""
        try:
            # Method 1: Try the image API with image-specific headers
            image_headers = {
                "Authorization": f"Bearer {self.lucid_api_key}",
                "Accept": "image/png",  # Accept PNG images
                "Lucid-Api-Version": "1"
            }
            
            # Try the document image endpoint first
            page_num = 1
            width = 1920
            square = 0
            
            image_url = (
                f"https://lucid.app/documents/image/"
                f"{diagram_id}/{page_num}/{width}/{square}"
            )
            
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(
                    image_url,
                    headers=image_headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return {
                        "image_data": response.content,
                        "metadata": {
                            "format": "PNG",
                            "width": width,
                            "page_num": page_num,
                            "method": "direct_image_api"
                        }
                    }
                
                print(f"Direct image API failed: {response.status_code} - {response.text}")
                
                # Method 2: Try the export API with JSON headers
                json_headers = {
                    "Authorization": f"Bearer {self.lucid_api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Lucid-Api-Version": "1"
                }
                
                export_response = await client.post(
                    f"https://api.lucid.co/documents/{diagram_id}/export",
                    headers=json_headers,
                    json={
                        "format": "PNG",
                        "pageSelection": "ALL",
                        "scale": 2
                    },
                    timeout=30.0
                )
                
                if export_response.status_code == 200:
                    export_data = export_response.json()
                    export_url = export_data.get("url")
                    
                    if export_url:
                        # Download from export URL
                        download_response = await client.get(export_url, timeout=60.0)
                        if download_response.status_code == 200:
                            return {
                                "image_data": download_response.content,
                                "metadata": {
                                    "format": "PNG",
                                    "export_id": export_data.get("id"),
                                    "scale": 2,
                                    "method": "export_api"
                                }
                            }
                
                print(f"Export API also failed: {export_response.status_code}")
                
        except Exception as e:
            print(f"Error in all Lucid export methods: {e}")
        
        return None
    
    async def _download_and_save_lucid_export(
        self, 
        image_data: bytes,
        diagram_id: str, 
        diagram_title: str
    ) -> Optional[str]:
        """Save Lucid image data to temporary file"""
        try:
            # Create safe filename
            allowed_chars = (' ', '-', '_')
            safe_title = "".join(
                c for c in diagram_title 
                if c.isalnum() or c in allowed_chars
            ).rstrip()
            safe_title = safe_title.replace(' ', '_')
            
            filename = f"lucid_{diagram_id}_{safe_title}.png"
            file_path = os.path.join(self.temp_dir, filename)
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            print(f"✅ Saved Lucid export to: {file_path}")
            return file_path
        
        except Exception as e:
            print(f"Error saving Lucid image to file: {e}")
            return None
    
    async def _get_figma_image_data(self, file_key: str) -> Optional[bytes]:
        """Get Figma image data using API"""
        try:
            async with httpx.AsyncClient(verify=False) as client:
                # Get image URL from Figma API
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
                            return img_response.content
                else:
                    print(f"Figma API error: {response.status_code} - "
                          f"{response.text}")
        
        except Exception as e:
            print(f"Error getting Figma image data: {e}")
        
        return None
    
    async def _save_figma_image_to_file(
        self, 
        image_data: bytes, 
        file_key: str, 
        file_name: str
    ) -> Optional[str]:
        """Save Figma image data to temporary file"""
        try:
            # Create safe filename
            safe_name = "".join(
                c for c in file_name if c.isalnum() or c in (' ', '-', '_')
            ).rstrip()
            safe_name = safe_name.replace(' ', '_')
            
            filename = f"figma_{file_key}_{safe_name}.png"
            file_path = os.path.join(self.temp_dir, filename)
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            print(f"✅ Saved Figma export to: {file_path}")
            return file_path
        
        except Exception as e:
            print(f"Error saving Figma image to file: {e}")
            return None
    
    async def _get_figma_file_metadata(self, file_key: str) -> Dict[str, Any]:
        """Get Figma file metadata"""
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(
                    f"https://api.figma.com/v1/files/{file_key}",
                    headers={"X-Figma-Token": self.figma_token},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    document = data.get("document", {})
                    
                    return {
                        "document_name": document.get("name", "Unknown"),
                        "last_modified": data.get("lastModified", "Unknown"),
                        "version": data.get("version", "Unknown"),
                        "pages": len(document.get("children", [])),
                        "description": document.get("description", "")
                    }
        
        except Exception as e:
            print(f"Error getting Figma metadata: {e}")
        
        return {}
    
    def cleanup_temp_files(self, file_paths: List[str]) -> None:
        """
        Clean up temporary files after analysis
        
        Args:
            file_paths: List of file paths to clean up
        """
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"🗑️  Cleaned up temporary file: {file_path}")
            except Exception as e:
                print(f"⚠️ Failed to clean up {file_path}: {e}")
    
    def cleanup_temp_directory(self) -> None:
        """Clean up entire temporary directory"""
        try:
            if self.temp_dir and os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir)
                print(f"🗑️  Cleaned up temporary directory: {self.temp_dir}")
                self.temp_dir = None
        except Exception as e:
            print(f"⚠️ Failed to clean up temp directory: {e}")
    
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
            import base64
            
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


# Create service instance
enhanced_visual_capture_service = EnhancedVisualCaptureService() 