"""
Cache Service for managing cached files and integrating with OpenArena
"""

import hashlib
import json
import time
import aiofiles
import base64
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

from app.core.config import settings


class CacheService:
    """Service for managing cached files with OpenArena integration"""
    
    def __init__(self):
        self.cache_enabled = settings.CACHE_ENABLED
        self.cache_dir = Path(settings.CACHE_DIR)
        self.cache_expiry_hours = settings.CACHE_EXPIRY_HOURS
        self.auto_upload = settings.AUTO_UPLOAD_TO_OPENARENA
        
        # Ensure cache directory exists
        if self.cache_enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(
        self, 
        document_id: str, 
        format: str = "png",
        page_id: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> str:
        """Generate a unique cache key for a document export"""
        key_parts = [document_id, format]
        if page_id:
            key_parts.append(f"page_{page_id}")
        if width:
            key_parts.append(f"w_{width}")
        if height:
            key_parts.append(f"h_{height}")
        
        key_string = "_".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_cache_paths(self, cache_key: str, format: str) -> Dict[str, Path]:
        """Get cache file paths for data and metadata"""
        ext = format.lower()
        if ext in ['jpg', 'jpeg']:
            ext = 'jpg'
        
        return {
            "data": self.cache_dir / f"{cache_key}.{ext}",
            "metadata": self.cache_dir / f"{cache_key}.json"
        }
    
    async def get_cached_export(
        self, 
        document_id: str,
        format: str = "png",
        page_id: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached export if it exists and is not expired
        
        Returns:
            Dictionary with cached data or None if not found/expired
        """
        if not self.cache_enabled:
            return None
        
        cache_key = self._get_cache_key(
            document_id, format, page_id, width, height
        )
        paths = self._get_cache_paths(cache_key, format)
        
        try:
            # Check if both files exist
            if not paths["data"].exists() or not paths["metadata"].exists():
                return None
            
            # Read metadata
            async with aiofiles.open(paths["metadata"], 'r') as f:
                metadata_content = await f.read()
                metadata = json.loads(metadata_content)
            
            # Check expiry
            cached_time = metadata.get("cached_at", 0)
            expiry_time = cached_time + (self.cache_expiry_hours * 3600)
            
            if time.time() > expiry_time:
                # Cache expired, clean up
                await self._cleanup_cache_entry(cache_key, format)
                return None
            
            # Read cached data
            async with aiofiles.open(paths["data"], 'rb') as f:
                image_data = await f.read()
            
            print(f"📋 Cache hit for document {document_id}")
            
            return {
                "success": True,
                "image_data": image_data,
                "metadata": metadata,
                "cached": True,
                "cache_key": cache_key,
                "file_path": str(paths["data"])
            }
            
        except Exception as e:
            print(f"⚠️ Error reading cache for {document_id}: {e}")
            return None
    
    async def cache_export(
        self,
        document_id: str,
        image_data: bytes,
        metadata: Dict[str, Any],
        format: str = "png",
        page_id: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Cache exported image data and metadata
        
        Returns:
            Dictionary with cache information and OpenArena upload result
        """
        if not self.cache_enabled:
            return {
                "cached": False,
                "reason": "Cache disabled"
            }
        
        try:
            cache_key = self._get_cache_key(
                document_id, format, page_id, width, height
            )
            paths = self._get_cache_paths(cache_key, format)
            
            # Prepare enhanced metadata
            enhanced_metadata = {
                **metadata,
                "cached_at": time.time(),
                "cache_key": cache_key,
                "document_id": document_id,
                "format": format,
                "page_id": page_id,
                "width": width,
                "height": height,
                "file_size": len(image_data)
            }
            
            # Write image data
            async with aiofiles.open(paths["data"], 'wb') as f:
                await f.write(image_data)
            
            # Write metadata
            async with aiofiles.open(paths["metadata"], 'w') as f:
                await f.write(json.dumps(enhanced_metadata, indent=2))
            
            print(f"💾 Cached export for document {document_id}")
            
            result = {
                "cached": True,
                "cache_key": cache_key,
                "file_path": str(paths["data"]),
                "metadata_path": str(paths["metadata"])
            }
            
            # Auto-upload to OpenArena if enabled
            if self.auto_upload:
                upload_result = await self._upload_to_openarena(
                    document_id, image_data, enhanced_metadata, format
                )
                result["openarena_upload"] = upload_result
            
            return result
            
        except Exception as e:
            print(f"⚠️ Error caching export for {document_id}: {e}")
            return {
                "cached": False,
                "error": str(e)
            }
    
    async def _upload_to_openarena(
        self,
        document_id: str,
        image_data: bytes,
        metadata: Dict[str, Any],
        format: str
    ) -> Dict[str, Any]:
        """Upload cached file to OpenArena"""
        try:
            # Import here to avoid circular imports
            from app.services.data_source_service import data_source_service
            
            # Convert to base64
            encoded_content = base64.b64encode(image_data).decode('utf-8')
            
            # Create filename
            page_info = (f"_page_{metadata['page_id']}" 
                         if metadata.get('page_id') else "")
            filename = f"lucid_{document_id}{page_info}.{format}"
            
            # Upload to OpenArena
            description = f"Cached Lucid export - Document ID: {document_id}"
            upload_result = await data_source_service.process_file_upload(
                file_name=filename,
                file_type=format,
                content=encoded_content,
                description=description
            )
            
            if upload_result.get("success"):
                print(f"📤 Auto-uploaded to OpenArena: {upload_result['file_id']}")
            
            return upload_result
            
        except Exception as e:
            print(f"⚠️ Error uploading to OpenArena: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _cleanup_cache_entry(self, cache_key: str, format: str) -> None:
        """Remove cache entry files"""
        try:
            paths = self._get_cache_paths(cache_key, format)
            for path in paths.values():
                if path.exists():
                    path.unlink()
            print(f"🗑️ Cleaned up expired cache entry: {cache_key}")
        except Exception as e:
            print(f"⚠️ Error cleaning cache entry {cache_key}: {e}")
    
    async def cleanup_expired_cache(self) -> Dict[str, Any]:
        """Clean up expired cache entries"""
        if not self.cache_enabled or not self.cache_dir.exists():
            return {"cleaned": 0, "errors": 0}
        
        cleaned = 0
        errors = 0
        current_time = time.time()
        
        try:
            # Get all metadata files
            metadata_files = list(self.cache_dir.glob("*.json"))
            
            for metadata_file in metadata_files:
                try:
                    async with aiofiles.open(metadata_file, 'r') as f:
                        content = await f.read()
                        metadata = json.loads(content)
                    
                    cached_time = metadata.get("cached_at", 0)
                    expiry_time = cached_time + (self.cache_expiry_hours * 3600)
                    
                    if current_time > expiry_time:
                        cache_key = metadata.get("cache_key")
                        format_type = metadata.get("format", "png")
                        
                        if cache_key:
                            await self._cleanup_cache_entry(cache_key, format_type)
                            cleaned += 1
                        
                except Exception as e:
                    print(f"⚠️ Error processing {metadata_file}: {e}")
                    errors += 1
            
            print(f"🧹 Cache cleanup completed: {cleaned} cleaned, {errors} errors")
            
        except Exception as e:
            print(f"⚠️ Error during cache cleanup: {e}")
            errors += 1
        
        return {"cleaned": cleaned, "errors": errors}
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self.cache_enabled or not self.cache_dir.exists():
            return {
                "enabled": False,
                "total_files": 0,
                "total_size": 0,
                "cache_dir": str(self.cache_dir)
            }
        
        try:
            files = list(self.cache_dir.iterdir())
            data_files = [f for f in files if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.pdf', '.svg']]
            metadata_files = [f for f in files if f.suffix == '.json']
            
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            
            return {
                "enabled": True,
                "cache_dir": str(self.cache_dir),
                "total_files": len(files),
                "data_files": len(data_files),
                "metadata_files": len(metadata_files),
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "expiry_hours": self.cache_expiry_hours,
                "auto_upload": self.auto_upload
            }
            
        except Exception as e:
            return {
                "enabled": True,
                "error": str(e),
                "cache_dir": str(self.cache_dir)
            }
    
    async def list_cached_documents(self) -> List[Dict[str, Any]]:
        """List all cached documents with metadata"""
        if not self.cache_enabled or not self.cache_dir.exists():
            return []
        
        cached_docs = []
        
        try:
            metadata_files = list(self.cache_dir.glob("*.json"))
            
            for metadata_file in metadata_files:
                try:
                    async with aiofiles.open(metadata_file, 'r') as f:
                        content = await f.read()
                        metadata = json.loads(content)
                    
                    cached_time = metadata.get("cached_at", 0)
                    expiry_time = cached_time + (self.cache_expiry_hours * 3600)
                    is_expired = time.time() > expiry_time
                    
                    cached_docs.append({
                        "document_id": metadata.get("document_id"),
                        "cache_key": metadata.get("cache_key"),
                        "format": metadata.get("format"),
                        "page_id": metadata.get("page_id"),
                        "file_size": metadata.get("file_size"),
                        "cached_at": datetime.fromtimestamp(cached_time).isoformat(),
                        "expires_at": datetime.fromtimestamp(expiry_time).isoformat(),
                        "is_expired": is_expired,
                        "file_path": str(self.cache_dir / f"{metadata.get('cache_key')}.{metadata.get('format')}")
                    })
                    
                except Exception as e:
                    print(f"⚠️ Error reading metadata from {metadata_file}: {e}")
            
            # Sort by cached time (newest first)
            cached_docs.sort(key=lambda x: x.get("cached_at", ""), reverse=True)
            
        except Exception as e:
            print(f"⚠️ Error listing cached documents: {e}")
        
        return cached_docs


# Global instance
cache_service = CacheService() 