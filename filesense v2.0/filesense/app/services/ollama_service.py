"""
OLLAMA Service for AI-powered file analysis
"""
import requests
import json
from typing import List, Dict, Optional, Tuple


class OllamaService:
    """Service for interacting with OLLAMA AI"""
    
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url.rstrip('/')
        self.default_model = "llama2"
    
    def is_running(self) -> bool:
        """Check if OLLAMA is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
        except Exception as e:
            print(f"Error getting models: {e}")
        return []
    
    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """Get information about a specific model"""
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": model_name},
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error getting model info: {e}")
        return None
    
    def generate_tags(self, text: str, model: Optional[str] = None, max_tags: int = 5) -> List[str]:
        """Generate tags for the given text"""
        if not model:
            model = self.default_model
        
        prompt = f"""Analyze the following text and provide {max_tags} relevant, descriptive tags.
Return ONLY a comma-separated list of tags, nothing else.

Text: {text[:2000]}

Tags:"""
        
        response = self._generate(prompt, model)
        
        if response:
            # Clean and parse tags
            tags = response.replace('\n', ',').replace('.', '').split(',')
            tags = [tag.strip().lstrip('-*•').strip() for tag in tags if tag.strip()]
            tags = [tag for tag in tags if len(tag) > 1 and len(tag) < 30]
            return tags[:max_tags]
        return []
    
    def generate_summary(self, text: str, model: Optional[str] = None, max_sentences: int = 3) -> str:
        """Generate a summary of the given text"""
        if not model:
            model = self.default_model
        
        prompt = f"""Summarize the following text in {max_sentences} concise sentences.
Focus on the key points and main ideas.

Text: {text[:3000]}

Summary:"""
        
        return self._generate(prompt, model) or ""
    
    def extract_insights(self, text: str, model: Optional[str] = None) -> List[Dict[str, str]]:
        """Extract key insights from the text"""
        if not model:
            model = self.default_model
        
        prompt = f"""Analyze the following text and extract 3-5 key insights.
For each insight, provide a title and description.
Format: Title: [title]
Description: [description]

Text: {text[:3000]}

Insights:"""
        
        response = self._generate(prompt, model)
        
        insights = []
        if response:
            lines = response.strip().split('\n')
            current_insight = {}
            
            for line in lines:
                line = line.strip()
                if line.startswith('Title:'):
                    if current_insight and 'title' in current_insight:
                        insights.append(current_insight)
                    current_insight = {'title': line.replace('Title:', '').strip()}
                elif line.startswith('Description:'):
                    if current_insight:
                        current_insight['description'] = line.replace('Description:', '').strip()
                elif line and current_insight.get('description'):
                    current_insight['description'] += ' ' + line
            
            if current_insight and 'title' in current_insight:
                insights.append(current_insight)
        
        return insights[:5]
    
    def categorize_file(self, filename: str, content: str = "", model: Optional[str] = None) -> str:
        """Categorize a file based on its name and content"""
        if not model:
            model = self.default_model
        
        prompt = f"""Categorize the following file into ONE of these categories:
- Documents (reports, letters, forms)
- Spreadsheets (data, finances, calculations)
- Presentations (slides, pitches)
- Code (programming files)
- Media (images, videos, audio)
- Archives (zip, compressed files)
- Personal (photos, notes, personal docs)
- Work (professional documents)
- Other

Filename: {filename}
Content preview: {content[:500] if content else "No preview available"}

Return ONLY the category name, nothing else.
Category:"""
        
        response = self._generate(prompt, model)
        
        if response:
            category = response.strip().split('\n')[0].strip()
            valid_categories = [
                'Documents', 'Spreadsheets', 'Presentations', 'Code', 
                'Media', 'Archives', 'Personal', 'Work', 'Other'
            ]
            for cat in valid_categories:
                if cat.lower() in category.lower():
                    return cat
        
        return "Other"
    
    def suggest_organization(self, files_info: List[Dict]) -> Dict[str, List[str]]:
        """Suggest file organization structure"""
        if not files_info:
            return {}
        
        # Build file list for prompt
        file_list = '\n'.join([
            f"- {f['name']} ({f.get('type', 'unknown')})"
            for f in files_info[:20]  # Limit to 20 files
        ])
        
        prompt = f"""Given these files, suggest an organization structure by grouping related files.
Provide folder names and which files belong in each folder.

Files:
{file_list}

Suggest 3-5 folder names and list which files belong in each.
Format:
Folder Name: [name]
Files: [file1], [file2], ...

Organization:"""
        
        response = self._generate(prompt, self.default_model)
        
        organization = {}
        if response:
            lines = response.strip().split('\n')
            current_folder = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('Folder Name:') or line.startswith('Folder:'):
                    current_folder = line.split(':', 1)[1].strip()
                    organization[current_folder] = []
                elif line.startswith('Files:') and current_folder:
                    files = line.split(':', 1)[1].strip()
                    organization[current_folder] = [
                        f.strip() for f in files.split(',')
                    ]
        
        return organization
    
    def analyze_file_content(self, content: str, model: Optional[str] = None) -> Dict:
        """Comprehensive file content analysis"""
        if not model:
            model = self.default_model
        
        return {
            'summary': self.generate_summary(content, model),
            'tags': self.generate_tags(content, model),
            'insights': self.extract_insights(content, model)
        }
    
    def _generate(self, prompt: str, model: str, stream: bool = False) -> Optional[str]:
        """Generate text using OLLAMA"""
        try:
            payload = {
                'model': model,
                'prompt': prompt,
                'stream': stream,
                'options': {
                    'temperature': 0.7,
                    'top_p': 0.9
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=300
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', '').strip()
            else:
                print(f"OLLAMA API error: {response.status_code}")
        except Exception as e:
            print(f"OLLAMA error: {e}")
        
        return None
    
    def pull_model(self, model_name: str) -> Tuple[bool, str]:
        """Pull/download a model from OLLAMA library"""
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=3600
            )
            
            if response.status_code == 200:
                return True, f"Model {model_name} pulled successfully"
            else:
                return False, f"Failed to pull model: {response.status_code}"
        except Exception as e:
            return False, f"Error pulling model: {str(e)}"
