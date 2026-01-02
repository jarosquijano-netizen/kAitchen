import requests
from bs4 import BeautifulSoup
import trafilatura
import re
import json
from typing import Dict, List, Optional
from urllib.parse import urlparse

class RecipeExtractor:
    """Extract recipe information from URLs"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def extract_from_url(self, url: str) -> Dict:
        """
        Extract recipe data from a URL
        Returns a dictionary with recipe information
        """
        try:
            # Handle Pinterest URLs - they redirect to the actual recipe site
            if 'pin.it' in url or 'pinterest.com' in url:
                return self._extract_from_pinterest(url)
            
            # Fetch the page
            response = requests.get(url, headers=self.headers, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to extract structured data (JSON-LD)
            recipe_data = self._extract_json_ld(soup)
            
            # If no structured data, try manual extraction
            if not recipe_data or not recipe_data.get('title'):
                recipe_data = self._manual_extraction(soup, url)
            
            # Extract text content with trafilatura
            text_content = trafilatura.extract(response.content)
            recipe_data['extracted_text'] = text_content
            
            # Add URL
            recipe_data['url'] = url
            recipe_data['source_domain'] = urlparse(url).netloc
            
            return recipe_data
            
        except Exception as e:
            return {
                'error': str(e),
                'url': url,
                'title': 'Error al extraer receta',
                'success': False
            }
    
    def _extract_from_pinterest(self, url: str) -> Dict:
        """
        Extract recipe from Pinterest URL
        Pinterest usually redirects to the actual recipe site
        """
        try:
            # Follow redirects to get to Pinterest page
            response = requests.get(url, headers=self.headers, timeout=15, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find the actual recipe URL from Pinterest
            # Pinterest often has the source URL in various places
            source_url = None
            
            # Method 1: Look for canonical link or og:url (but skip if it's Pinterest)
            canonical = soup.find('link', rel='canonical')
            if canonical and canonical.get('href'):
                href = canonical['href']
                if 'pinterest.com' not in href and 'pin.it' not in href:
                    source_url = href
            
            # Method 2: Look for og:url meta tag (but skip if it's Pinterest)
            if not source_url:
                og_url = soup.find('meta', property='og:url')
                if og_url and og_url.get('content'):
                    href = og_url['content']
                    if 'pinterest.com' not in href and 'pin.it' not in href:
                        source_url = href
            
            # Method 3: Look for external link in Pinterest's data
            if not source_url:
                # Try to find JSON data in script tags
                scripts = soup.find_all('script', type='application/json')
                for script in scripts:
                    try:
                        data = json.loads(script.string)
                        # Pinterest stores source URL in various places
                        if isinstance(data, dict):
                            # Look for url or source_url in nested structures
                            source_url = self._find_url_in_dict(data)
                            if source_url:
                                break
                    except:
                        continue
            
            # Method 4: Look for links with "Visit" or "Source" text
            if not source_url:
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link.get('href', '')
                    text = link.get_text().strip().lower()
                    if ('visit' in text or 'source' in text or 'ver' in text) and href.startswith('http'):
                        source_url = href
                        break
            
            # Method 5: Look for external domain links (not pinterest.com)
            # Prioritize links that look like recipe sites
            if not source_url:
                links = soup.find_all('a', href=True)
                priority_urls = []
                other_urls = []
                
                for link in links:
                    href = link.get('href', '')
                    # Skip Pinterest links and relative URLs
                    if not href.startswith('http'):
                        continue
                    if 'pinterest.com' in href or 'pin.it' in href:
                        continue
                    # Skip JavaScript files and other non-recipe URLs
                    if any(skip in href.lower() for skip in ['.js', 'javascript:', 'cookies', 'webapp', 'developer-tools']):
                        continue
                    
                    href_lower = href.lower()
                    # Check if it looks like a recipe site
                    is_recipe_site = any(domain in href_lower for domain in [
                        'recipe', 'cook', 'food', 'blog', 'takestwoeggs', 
                        'allrecipes', 'foodnetwork', 'tasty', 'delish',
                        'rechupete', 'directoalpaladar', 'tastyfunrecipes',
                        'sanacooks', 'majasrecipes', 'ncyclopaedia'
                    ])
                    
                    if is_recipe_site:
                        # Remove Pinterest tracking parameters
                        clean_url = href.split('?')[0].split('&')[0]
                        if clean_url not in priority_urls:
                            priority_urls.append(clean_url)
                    elif ('www.' in href or ('.com' in href and not any(skip in href for skip in ['pinimg', 'pinterest', 'javascript', '.js']))):
                        clean_url = href.split('?')[0].split('&')[0]
                        if clean_url not in other_urls:
                            other_urls.append(clean_url)
                
                # Use priority URL first, then fallback to others
                if priority_urls:
                    source_url = priority_urls[0]
                elif other_urls:
                    source_url = other_urls[0]
            
            # Method 6: Look in Pinterest's JSON data for external links
            if not source_url:
                # Pinterest stores recipe URLs in JSON-LD or script tags
                scripts = soup.find_all('script')
                for script in scripts:
                    script_text = script.string or ''
                    if not script_text:
                        continue
                    # Look for URLs in the script content - improved pattern
                    url_pattern = r'https?://[^\s"\'<>\)]+(?:recipe|cook|food|blog|tastyfunrecipes|takestwoeggs|allrecipes|\.com/[^\s"\'<>\)]+recipe)[^\s"\'<>\)]*'
                    matches = re.findall(url_pattern, script_text, re.I)
                    for match in matches:
                        # Clean the match
                        clean_match = match.split('"')[0].split("'")[0].split('\\')[0].split(')')[0].split('}')[0]
                        if 'pinterest.com' not in clean_match and 'pin.it' not in clean_match:
                            # Skip JavaScript files
                            if not any(skip in clean_match.lower() for skip in ['.js', 'javascript:', 'cookies', 'webapp']):
                                source_url = clean_match
                                break
                    if source_url:
                        break
            
            # Method 7: Look for og:url that points to external site
            if not source_url:
                og_url_tag = soup.find('meta', property='og:url')
                if og_url_tag:
                    og_url = og_url_tag.get('content', '')
                    if og_url and 'pinterest.com' not in og_url and 'pin.it' not in og_url:
                        # Check if it's a real recipe site
                        if any(domain in og_url.lower() for domain in ['recipe', 'cook', 'food', 'blog', '.com']):
                            if not any(skip in og_url.lower() for skip in ['.js', 'javascript', 'cookies']):
                                source_url = og_url
            
            # If we found a source URL, extract from there
            if source_url:
                # Clean the URL (remove Pinterest tracking params)
                source_url = source_url.split('?')[0].split('&')[0]
                
                # Try to extract from the source site
                try:
                    source_response = requests.get(source_url, headers=self.headers, timeout=15, allow_redirects=True)
                    source_response.raise_for_status()
                    
                    source_soup = BeautifulSoup(source_response.content, 'html.parser')
                    
                    # Try structured data first
                    recipe_data = self._extract_json_ld(source_soup)
                    
                    # If no structured data, try manual extraction
                    if not recipe_data or not recipe_data.get('title'):
                        recipe_data = self._manual_extraction(source_soup, source_url)
                    
                    # Extract images and videos from source site if not already found
                    if not recipe_data.get('image_url'):
                        # Try to find images in source page
                        img_tags = source_soup.find_all('img', src=True)
                        for img in img_tags[:5]:  # Limit to first 5
                            src = img.get('src', '')
                            if src.startswith('http') or src.startswith('//'):
                                if not src.startswith('http'):
                                    src = 'https:' + src
                                if 'image' in img.get('class', []) or any(keyword in src.lower() for keyword in ['recipe', 'food', 'dish', 'meal']):
                                    recipe_data['image_url'] = src
                                    break
                    
                    # Add Pinterest info
                    recipe_data['pinterest_url'] = url
                    recipe_data['source_url'] = source_url
                    recipe_data['url'] = source_url  # Use source URL as primary
                    recipe_data['source_domain'] = urlparse(source_url).netloc
                    
                    return recipe_data
                    
                except Exception as e:
                    # If source extraction fails, try to extract from Pinterest page itself
                    pass
            
            # Fallback: Try to extract from Pinterest page directly
            # Pinterest sometimes has recipe data in meta tags or JSON
            recipe_data = {
                'title': '',
                'ingredients': [],
                'instructions': '',
                'success': True
            }
            
            # Try to get title from Pinterest
            title_tag = soup.find('h1') or soup.find('title')
            if title_tag:
                title_text = title_tag.get_text().strip()
                # Clean Pinterest title (remove "on Pinterest" etc)
                title_text = re.sub(r'\s*on\s+Pinterest.*$', '', title_text, flags=re.I)
                recipe_data['title'] = title_text
            
            # Try to extract description
            desc_tag = soup.find('meta', property='og:description')
            if desc_tag and desc_tag.get('content'):
                recipe_data['description'] = desc_tag['content']
            
            # Try to extract images from multiple sources
            images = []
            videos = []
            
            # Method 1: og:image meta tag
            img_tag = soup.find('meta', property='og:image')
            if img_tag and img_tag.get('content'):
                images.append(img_tag['content'])
            
            # Method 2: Look for Pinterest image in JSON data
            scripts = soup.find_all('script', type='application/json')
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    # Search for image URLs in nested data
                    img_urls = self._find_images_in_dict(data)
                    images.extend(img_urls)
                    
                    # Search for video URLs
                    video_urls = self._find_videos_in_dict(data)
                    videos.extend(video_urls)
                except:
                    continue
            
            # Method 3: Look for img tags with Pinterest classes or data attributes
            img_tags = soup.find_all('img', src=True)
            for img in img_tags:
                src = img.get('src', '') or img.get('data-src', '') or img.get('data-lazy-src', '')
                if src:
                    # Clean Pinterest image URLs (remove size parameters)
                    if 'pinimg.com' in src or 'pinterest.com' in src:
                        # Remove size parameters like /236x/ or /564x/
                        src = re.sub(r'/\d+x\d*/', '/originals/', src)
                        if src not in images:
                            images.append(src)
                    elif src.startswith('http') and any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                        if src not in images:
                            images.append(src)
            
            # Method 4: Look for video tags
            video_tags = soup.find_all('video', src=True)
            for video in video_tags:
                src = video.get('src', '')
                if src and src not in videos:
                    videos.append(src)
            
            # Also check for source tags inside video
            video_containers = soup.find_all('video')
            for video in video_containers:
                sources = video.find_all('source', src=True)
                for source in sources:
                    src = source.get('src', '')
                    if src and src not in videos:
                        videos.append(src)
            
            # Set primary image (first one found)
            if images:
                recipe_data['image_url'] = images[0]
                recipe_data['images'] = images  # Store all images
            
            # Set video if found
            if videos:
                recipe_data['video_url'] = videos[0]
                recipe_data['videos'] = videos  # Store all videos
            
            recipe_data['pinterest_url'] = url
            recipe_data['url'] = url
            recipe_data['source_domain'] = 'pinterest.com'
            recipe_data['note'] = 'Receta extraída de Pinterest. Puede que necesites visitar el sitio original para ver ingredientes e instrucciones completas.'
            
            return recipe_data
            
        except Exception as e:
            return {
                'error': f'Error al extraer receta de Pinterest: {str(e)}',
                'url': url,
                'title': 'Error al extraer receta de Pinterest',
                'success': False
            }
    
    def _find_url_in_dict(self, data: dict, max_depth: int = 5) -> Optional[str]:
        """Recursively search for URL in nested dictionary"""
        if max_depth <= 0:
            return None
        
        for key, value in data.items():
            if isinstance(value, str) and value.startswith('http') and 'pinterest.com' not in value:
                return value
            elif isinstance(value, dict):
                result = self._find_url_in_dict(value, max_depth - 1)
                if result:
                    return result
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        result = self._find_url_in_dict(item, max_depth - 1)
                        if result:
                            return result
        
        return None
    
    def _find_images_in_dict(self, data: dict, max_depth: int = 5, found: list = None) -> list:
        """Recursively search for image URLs in nested dictionary"""
        if found is None:
            found = []
        if max_depth <= 0:
            return found
        
        for key, value in data.items():
            if isinstance(value, str):
                # Look for image URLs
                if value.startswith('http') and any(ext in value.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', 'pinimg.com', 'image']):
                    if value not in found:
                        found.append(value)
            elif isinstance(value, dict):
                self._find_images_in_dict(value, max_depth - 1, found)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._find_images_in_dict(item, max_depth - 1, found)
                    elif isinstance(item, str) and item.startswith('http') and any(ext in item.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                        if item not in found:
                            found.append(item)
        
        return found
    
    def _find_videos_in_dict(self, data: dict, max_depth: int = 5, found: list = None) -> list:
        """Recursively search for video URLs in nested dictionary"""
        if found is None:
            found = []
        if max_depth <= 0:
            return found
        
        for key, value in data.items():
            if isinstance(value, str):
                # Look for video URLs
                if value.startswith('http') and any(ext in value.lower() for ext in ['.mp4', '.webm', '.mov', 'video', 'youtube.com', 'youtu.be', 'vimeo.com']):
                    if value not in found:
                        found.append(value)
            elif isinstance(value, dict):
                self._find_videos_in_dict(value, max_depth - 1, found)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._find_videos_in_dict(item, max_depth - 1, found)
                    elif isinstance(item, str) and item.startswith('http') and any(ext in item.lower() for ext in ['.mp4', '.webm', '.mov', 'video']):
                        if item not in found:
                            found.append(item)
        
        return found
    
    def _extract_json_ld(self, soup: BeautifulSoup) -> Dict:
        """Extract recipe data from JSON-LD structured data"""
        recipe_data = {}
        
        # Find JSON-LD script tags
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                
                # Handle @graph structure
                if isinstance(data, dict) and '@graph' in data:
                    data = data['@graph']
                
                # Handle list
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get('@type') == 'Recipe':
                            data = item
                            break
                
                # Check if it's a Recipe
                if isinstance(data, dict) and data.get('@type') == 'Recipe':
                    recipe_data = self._parse_recipe_schema(data)
                    break
                    
            except json.JSONDecodeError:
                continue
        
        return recipe_data
    
    def _parse_recipe_schema(self, schema: Dict) -> Dict:
        """Parse Recipe schema.org structured data"""
        recipe = {
            'title': schema.get('name', ''),
            'description': schema.get('description', ''),
            'image_url': self._get_image_url(schema.get('image')),
            'prep_time': self._parse_duration(schema.get('prepTime')),
            'cook_time': self._parse_duration(schema.get('cookTime')),
            'total_time': self._parse_duration(schema.get('totalTime')),
            'servings': self._parse_servings(schema.get('recipeYield')),
            'cuisine_type': schema.get('recipeCuisine', ''),
            'difficulty': schema.get('difficulty', ''),
            'success': True
        }
        
        # Extract ingredients
        ingredients = []
        recipe_ingredients = schema.get('recipeIngredient', [])
        if isinstance(recipe_ingredients, list):
            ingredients = recipe_ingredients
        elif isinstance(recipe_ingredients, str):
            ingredients = [recipe_ingredients]
        recipe['ingredients'] = ingredients
        
        # Extract instructions
        instructions = []
        recipe_instructions = schema.get('recipeInstructions', [])
        
        if isinstance(recipe_instructions, list):
            for step in recipe_instructions:
                if isinstance(step, dict):
                    if step.get('@type') == 'HowToStep':
                        instructions.append(step.get('text', ''))
                    else:
                        instructions.append(str(step))
                elif isinstance(step, str):
                    instructions.append(step)
        elif isinstance(recipe_instructions, str):
            instructions = [recipe_instructions]
        
        recipe['instructions'] = '\n'.join(instructions) if instructions else ''
        
        return recipe
    
    def _manual_extraction(self, soup: BeautifulSoup, url: str) -> Dict:
        """Manual extraction when structured data is not available"""
        recipe = {
            'title': '',
            'ingredients': [],
            'instructions': '',
            'success': True
        }
        
        # Try to find title
        title_tag = soup.find('h1')
        if title_tag:
            recipe['title'] = title_tag.get_text().strip()
        else:
            # Fallback to page title
            title_tag = soup.find('title')
            if title_tag:
                recipe['title'] = title_tag.get_text().strip()
        
        # Try to find ingredients
        ingredients_section = soup.find(['div', 'section', 'ul'], 
                                       class_=re.compile(r'ingredient', re.I))
        if ingredients_section:
            ingredient_items = ingredients_section.find_all(['li', 'p'])
            recipe['ingredients'] = [item.get_text().strip() for item in ingredient_items]
        
        # Try to find instructions
        instructions_section = soup.find(['div', 'section', 'ol'], 
                                        class_=re.compile(r'instruction|preparation|step', re.I))
        if instructions_section:
            instruction_items = instructions_section.find_all(['li', 'p'])
            recipe['instructions'] = '\n'.join([item.get_text().strip() for item in instruction_items])
        
        # Try to find image
        img_tag = soup.find('img', class_=re.compile(r'recipe|featured|main', re.I))
        if img_tag and img_tag.get('src'):
            recipe['image_url'] = img_tag['src']
        
        return recipe
    
    def _get_image_url(self, image_data) -> str:
        """Extract image URL from various formats"""
        if isinstance(image_data, str):
            return image_data
        elif isinstance(image_data, dict):
            return image_data.get('url', '')
        elif isinstance(image_data, list) and len(image_data) > 0:
            if isinstance(image_data[0], str):
                return image_data[0]
            elif isinstance(image_data[0], dict):
                return image_data[0].get('url', '')
        return ''
    
    def _parse_duration(self, duration: str) -> Optional[int]:
        """Parse ISO 8601 duration to minutes"""
        if not duration:
            return None
        
        # ISO 8601: PT1H30M = 1 hour 30 minutes
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?'
        match = re.search(pattern, str(duration))
        
        if match:
            hours = int(match.group(1) or 0)
            minutes = int(match.group(2) or 0)
            return hours * 60 + minutes
        
        return None
    
    def _parse_servings(self, yield_data) -> Optional[int]:
        """Parse servings/yield data"""
        if not yield_data:
            return None
        
        if isinstance(yield_data, int):
            return yield_data
        
        if isinstance(yield_data, str):
            # Try to extract number
            match = re.search(r'\d+', yield_data)
            if match:
                return int(match.group())
        
        return None
    
    def extract_multiple_urls(self, urls: List[str]) -> List[Dict]:
        """Extract recipes from multiple URLs"""
        recipes = []
        
        for url in urls:
            print(f"Extrayendo receta de: {url}")
            recipe = self.extract_from_url(url)
            recipes.append(recipe)
        
        return recipes
