"""
Duplicate Finder - Detect duplicate files
"""
import os
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Callable
from collections import defaultdict
from app.models import File, get_session


class DuplicateFinder:
    """Find duplicate files by content hash"""
    
    @staticmethod
    def find_duplicates_in_database(progress_callback: Optional[Callable] = None) -> Dict[str, List[dict]]:
        """
        Find duplicate files in the database by calculating content hashes.
        Returns dict: {hash: [file_info, ...]}
        """
        session = get_session()
        files = session.query(File).all()
        
        # Group by size first (optimization - different sizes can't be duplicates)
        size_groups = defaultdict(list)
        for file in files:
            if file.size and file.size > 0:
                size_groups[file.size].append(file)
        
        # For groups with same size, calculate hashes
        hash_groups = defaultdict(list)
        total_to_check = sum(len(files) for files in size_groups.values() if len(files) > 1)
        checked = 0
        
        for size, files in size_groups.items():
            if len(files) < 2:
                continue
            
            for file in files:
                if progress_callback:
                    checked += 1
                    progress_callback(checked, total_to_check, file.name)
                
                if not os.path.exists(file.path):
                    continue
                
                file_hash = DuplicateFinder._calculate_hash(file.path)
                if file_hash:
                    hash_groups[file_hash].append({
                        'id': file.id,
                        'name': file.name,
                        'path': file.path,
                        'size': file.size,
                        'size_formatted': file.size_formatted,
                        'modified': file.last_modified
                    })
        
        # Filter to only groups with duplicates
        duplicates = {
            h: files for h, files in hash_groups.items()
            if len(files) > 1
        }
        
        return duplicates
    
    @staticmethod
    def find_duplicates_in_folder(folder_path: str, recursive: bool = True,
                                   progress_callback: Optional[Callable] = None) -> Dict[str, List[str]]:
        """
        Find duplicate files in a folder.
        Returns dict: {hash: [file_paths, ...]}
        """
        if not os.path.exists(folder_path):
            return {}
        
        # Collect all files
        files = []
        if recursive:
            for root, _, filenames in os.walk(folder_path):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
        else:
            for item in os.listdir(folder_path):
                path = os.path.join(folder_path, item)
                if os.path.isfile(path):
                    files.append(path)
        
        # Group by size
        size_groups = defaultdict(list)
        for file_path in files:
            try:
                size = os.path.getsize(file_path)
                if size > 0:
                    size_groups[size].append(file_path)
            except (OSError, IOError):
                pass
        
        # Calculate hashes for potential duplicates
        hash_groups = defaultdict(list)
        total_to_check = sum(len(paths) for paths in size_groups.values() if len(paths) > 1)
        checked = 0
        
        for size, paths in size_groups.items():
            if len(paths) < 2:
                continue
            
            for file_path in paths:
                if progress_callback:
                    checked += 1
                    progress_callback(checked, total_to_check, os.path.basename(file_path))
                
                file_hash = DuplicateFinder._calculate_hash(file_path)
                if file_hash:
                    hash_groups[file_hash].append(file_path)
        
        # Filter to only groups with duplicates
        duplicates = {
            h: paths for h, paths in hash_groups.items()
            if len(paths) > 1
        }
        
        return duplicates
    
    @staticmethod
    def find_similar_names(similarity_threshold: float = 0.8) -> List[Tuple[dict, dict, float]]:
        """
        Find files with similar names.
        Returns list of tuples: (file1_info, file2_info, similarity_score)
        """
        session = get_session()
        files = session.query(File).all()
        
        similar_pairs = []
        
        for i, file1 in enumerate(files):
            for file2 in files[i+1:]:
                similarity = DuplicateFinder._name_similarity(file1.name, file2.name)
                
                if similarity >= similarity_threshold:
                    similar_pairs.append((
                        {'id': file1.id, 'name': file1.name, 'path': file1.path},
                        {'id': file2.id, 'name': file2.name, 'path': file2.path},
                        similarity
                    ))
        
        # Sort by similarity (highest first)
        similar_pairs.sort(key=lambda x: x[2], reverse=True)
        return similar_pairs
    
    @staticmethod
    def get_duplicate_stats(duplicates: Dict[str, List]) -> dict:
        """Get statistics about duplicate files"""
        if not duplicates:
            return {
                'duplicate_groups': 0,
                'duplicate_files': 0,
                'wasted_space': 0,
                'wasted_space_formatted': '0 B'
            }
        
        total_files = sum(len(files) for files in duplicates.values())
        total_groups = len(duplicates)
        
        # Calculate wasted space (all but one copy in each group)
        wasted_space = 0
        for files in duplicates.values():
            if files and isinstance(files[0], dict) and 'size' in files[0]:
                file_size = files[0]['size']
                wasted_space += file_size * (len(files) - 1)
            elif files and isinstance(files[0], str):
                try:
                    file_size = os.path.getsize(files[0])
                    wasted_space += file_size * (len(files) - 1)
                except:
                    pass
        
        # Format wasted space
        if wasted_space < 1024:
            wasted_formatted = f"{wasted_space} B"
        elif wasted_space < 1024 * 1024:
            wasted_formatted = f"{wasted_space / 1024:.1f} KB"
        elif wasted_space < 1024 * 1024 * 1024:
            wasted_formatted = f"{wasted_space / (1024 * 1024):.1f} MB"
        else:
            wasted_formatted = f"{wasted_space / (1024 * 1024 * 1024):.2f} GB"
        
        return {
            'duplicate_groups': total_groups,
            'duplicate_files': total_files,
            'wasted_space': wasted_space,
            'wasted_space_formatted': wasted_formatted
        }
    
    @staticmethod
    def _calculate_hash(file_path: str, chunk_size: int = 8192) -> Optional[str]:
        """Calculate MD5 hash of a file"""
        try:
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            return None
    
    @staticmethod
    def _name_similarity(name1: str, name2: str) -> float:
        """
        Calculate similarity between two filenames (0-1).
        Uses Levenshtein distance ratio.
        """
        # Remove extensions for comparison
        stem1 = Path(name1).stem.lower()
        stem2 = Path(name2).stem.lower()
        
        # Simple Levenshtein-like similarity
        if stem1 == stem2:
            return 1.0
        
        # Length difference penalty
        len_diff = abs(len(stem1) - len(stem2))
        if len_diff > max(len(stem1), len(stem2)) * 0.5:
            return 0.0
        
        # Count matching characters in sequence
        matches = 0
        shorter = stem1 if len(stem1) <= len(stem2) else stem2
        longer = stem2 if len(stem1) <= len(stem2) else stem1
        
        for i, char in enumerate(shorter):
            if i < len(longer) and char == longer[i]:
                matches += 1
        
        similarity = matches / max(len(stem1), len(stem2))
        return similarity
    
    @staticmethod
    def compare_files(path1: str, path2: str) -> dict:
        """Compare two files and return comparison info"""
        result = {
            'identical': False,
            'same_size': False,
            'same_name': False,
            'file1': None,
            'file2': None
        }
        
        try:
            stat1 = os.stat(path1)
            stat2 = os.stat(path2)
            
            result['file1'] = {
                'path': path1,
                'name': os.path.basename(path1),
                'size': stat1.st_size,
                'modified': stat1.st_mtime
            }
            
            result['file2'] = {
                'path': path2,
                'name': os.path.basename(path2),
                'size': stat2.st_size,
                'modified': stat2.st_mtime
            }
            
            result['same_size'] = stat1.st_size == stat2.st_size
            result['same_name'] = os.path.basename(path1) == os.path.basename(path2)
            
            if result['same_size']:
                hash1 = DuplicateFinder._calculate_hash(path1)
                hash2 = DuplicateFinder._calculate_hash(path2)
                result['identical'] = hash1 == hash2 and hash1 is not None
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
