from fasthtml.common import *
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import time
import re

# Create FastHTML app
app = FastHTML()

def analyze_page(url):
    """Analyze a web page and return results as a list of strings"""
    result = [f"Analyzing {url}...", "-" * 40]
    
    # Performance metrics
    total_size = 0
    image_count = 0
    large_images = []
    css_count = 0
    js_count = 0
    external_requests = 0
    
    try:
        # Create a request with proper headers to avoid 403 errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Measure page loading time
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        load_time = time.time() - start_time
        
        # Calculate page size
        page_size_kb = len(response.content) / 1024
        total_size += page_size_kb
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # === PERFORMANCE ANALYSIS ===
        result.append("📊 PERFORMANCE METRICS")
        result.append(f"⏱️ Page Load Time: {load_time:.2f} seconds")
        result.append(f"📦 HTML Size: {page_size_kb:.1f} KB")
        
        # Performance recommendations based on load time
        if load_time > 3.0:
            result.append("🚨 SLOW: Page load time > 3 seconds")
        elif load_time > 1.0:
            result.append("⚠️ MODERATE: Page load time > 1 second")
        else:
            result.append("✅ FAST: Good page load time")
        
        # === SEO ANALYSIS ===
        result.append("\n🔍 SEO ANALYSIS")
        
        # Check H1 tag
        h1_tags = soup.find_all("h1")
        if len(h1_tags) == 1:
            result.append("✅ Exactly one <h1> tag found.")
        elif len(h1_tags) == 0:
            result.append("❌ Missing <h1> tag.")
        else:
            result.append(f"❌ Multiple <h1> tags found: {len(h1_tags)}")
        
        # Meta description check
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            desc_length = len(meta_desc.get("content"))
            result.append(f"✅ Meta description present ({desc_length} chars).")
            if desc_length > 160:
                result.append("⚠️ Meta description too long (>160 chars)")
            elif desc_length < 120:
                result.append("⚠️ Meta description too short (<120 chars)")
        else:
            result.append("❌ Meta description missing.")
        
        # Title tag check
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            title_length = len(title_tag.string)
            result.append(f"✅ Title tag present ({title_length} chars).")
            if title_length > 60:
                result.append("⚠️ Title too long (>60 chars)")
            elif title_length < 30:
                result.append("⚠️ Title too short (<30 chars)")
        else:
            result.append("❌ Title tag missing.")
        
        # Canonical tag
        canonical = soup.find("link", rel="canonical")
        result.append("✅ Canonical tag found." if canonical else "❌ Canonical tag missing.")
        
        # === RESOURCE ANALYSIS ===
        result.append("\n📁 RESOURCE ANALYSIS")
        
        # CSS files
        css_links = soup.find_all("link", rel="stylesheet")
        css_count = len(css_links)
        result.append(f"🎨 CSS Files: {css_count}")
        
        # List all CSS files
        if css_links:
            result.append("🎨 CSS Files Found:")
            for i, link in enumerate(css_links, 1):
                href = link.get("href", "")
                # Clean up the URL display
                display_href = href
                if href.startswith("//"):
                    display_href = "https:" + href
                elif href.startswith("/"):
                    display_href = f"{url.rstrip('/')}{href}"
                
                result.append(f"   {i}. {display_href}")
        
        if css_count > 5:
            result.append("⚠️ Too many CSS files - consider combining")
        elif css_count > 3:
            result.append("💡 Consider combining some CSS files")
        
        # JavaScript files
        js_scripts = soup.find_all("script", src=True)
        js_count = len(js_scripts)
        result.append(f"⚡ JavaScript Files: {js_count}")
        
        # List all JS files
        if js_scripts:
            result.append("📜 JavaScript Files Found:")
            for i, script in enumerate(js_scripts, 1):
                src = script.get("src", "")
                # Clean up the URL display
                display_src = src
                if src.startswith("//"):
                    display_src = "https:" + src
                elif src.startswith("/"):
                    display_src = f"{url.rstrip('/')}{src}"
                
                result.append(f"   {i}. {display_src}")
        
        if js_count > 10:
            result.append("⚠️ Too many JS files - consider bundling")
        elif js_count > 5:
            result.append("💡 Consider bundling some JS files")
        
        # External resources
        for link in css_links:
            href = link.get("href", "")
            if href.startswith("http") and not any(domain in href for domain in [url]):
                external_requests += 1
        
        for script in js_scripts:
            src = script.get("src", "")
            if src.startswith("http") and not any(domain in src for domain in [url]):
                external_requests += 1
        
        if external_requests > 0:
            result.append(f"🌐 External Resources: {external_requests}")
            if external_requests > 10:
                result.append("⚠️ Too many external requests - impacts loading speed")
        
        # === IMAGE ANALYSIS ===
        result.append("\n🖼️ IMAGE ANALYSIS")
        images = soup.find_all("img")
        image_count = len(images)
        result.append(f"📸 Total Images: {image_count}")
        
        for img in images:
            src = img.get("src")
            alt = img.get("alt")
            
            # Check alt text
            if not alt or alt.strip() == "":
                result.append(f"❌ Image missing alt text: {src}")
            
            # Check image sizes
            if src and src.startswith("https"):
                try:
                    img_response = requests.get(src, headers=headers, timeout=5)
                    size_kb = len(img_response.content) / 1024
                    total_size += size_kb
                    
                    if size_kb > 200:
                        large_images.append((src, size_kb))
                        result.append(f"⚠️ Large image (>{200}KB): {src} — {size_kb:.1f} KB")
                    
                    # Check for WebP format
                    if not src.endswith(('.webp', '.avif')):
                        result.append(f"💡 Consider WebP format for: {src}")
                        
                except Exception as e:
                    result.append(f"⚠️ Failed to load image: {src} — {e}")
        
        # === OPTIMIZATION RECOMMENDATIONS ===
        result.append("\n🚀 OPTIMIZATION RECOMMENDATIONS")
        
        recommendations = []
        
        # Performance-based recommendations
        if load_time > 2.0:
            recommendations.append("⚡ Enable GZIP/Brotli compression")
            recommendations.append("⚡ Use a Content Delivery Network (CDN)")
            recommendations.append("⚡ Minimize HTTP requests")
        
        if page_size_kb > 500:
            recommendations.append("📦 Minify HTML, CSS, and JavaScript")
            recommendations.append("📦 Remove unused CSS and JavaScript")
        
        if css_count > 3:
            recommendations.append("🎨 Combine CSS files to reduce requests")
        
        if js_count > 5:
            recommendations.append("⚡ Bundle JavaScript files")
            recommendations.append("⚡ Consider lazy loading for non-critical JS")
        
        if large_images:
            recommendations.append("🖼️ Optimize images (compress, resize, use WebP)")
            recommendations.append("🖼️ Implement lazy loading for images")
        
        if image_count > 20:
            recommendations.append("🖼️ Consider image sprites for small icons")
        
        if external_requests > 5:
            recommendations.append("🌐 Reduce external dependencies")
            recommendations.append("🌐 Self-host critical resources")
        
        # Browser caching
        recommendations.append("💾 Set proper browser caching headers")
        recommendations.append("💾 Use browser caching for static assets")
        
        # Additional recommendations
        recommendations.append("🔧 Enable browser caching")
        recommendations.append("🔧 Preload critical resources")
        recommendations.append("🔧 Use resource hints (dns-prefetch, preconnect)")
        
        if recommendations:
            for rec in recommendations[:8]:  # Show top 8 recommendations
                result.append(rec)
        else:
            result.append("✅ Page appears well optimized!")
        
        # === ACCESSIBILITY CHECK ===
        result.append("\n♿ ACCESSIBILITY")
        
        # Onclick buttons
        buttons_with_onclick = soup.find_all("button", onclick=True)
        if buttons_with_onclick:
            result.append("🖱️ <button> elements with 'onclick' actions:")
            for i, button in enumerate(buttons_with_onclick, start=1):
                onclick = button.get("onclick")
                result.append(f"   {i}. <button> — onclick=\"{onclick}\"")
        else:
            result.append("ℹ️ No <button> elements with 'onclick' attributes found.")
        
        # === SUMMARY ===
        result.append(f"\n📋 SUMMARY")
        result.append(f"Total Page Weight: {total_size:.1f} KB")
        result.append(f"Load Time: {load_time:.2f}s")
        result.append(f"Resources: {css_count} CSS, {js_count} JS, {image_count} images")
        
        # Performance grade
        if load_time < 1.0 and total_size < 500:
            result.append("🏆 Performance Grade: A - Excellent")
        elif load_time < 2.0 and total_size < 1000:
            result.append("🥈 Performance Grade: B - Good")
        elif load_time < 3.0 and total_size < 2000:
            result.append("🥉 Performance Grade: C - Needs Improvement")
        else:
            result.append("🚨 Performance Grade: D - Poor, needs optimization")
        
        result.append("✅ Analysis complete.")
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            result.append(f"❌ Access denied (403 Forbidden): {url}")
            result.append("   This website is blocking automated requests.")
            result.append("   Try accessing the site manually to check if it loads.")
        else:
            result.append(f"❌ HTTP Error {e.response.status_code}: {url}")
    except requests.exceptions.Timeout:
        result.append(f"❌ Request timed out: {url}")
    except requests.exceptions.ConnectionError:
        result.append(f"❌ Connection failed: {url}")
    except Exception as e:
        result.append(f"❌ Failed to analyze {url}: {e}")
    
    return result

@app.route("/")
def home():
    """Main page with URL input form"""
    return Titled("Web Page Analyzer",
        Card(
            H2("Web Page SEO & Accessibility Analyzer"),
            P("Enter a URL to analyze its SEO and accessibility features:"),
            Form(
                Input(
                    type="url", 
                    name="url", 
                    placeholder="https://example.com",
                    required=True,
                    style="width: 100%; padding: 10px; margin: 10px 0;"
                ),
                Button(
                    "Analyze Page", 
                    type="submit",
                    style="padding: 10px 20px; background: #007acc; color: white; border: none; cursor: pointer;"
                ),
                **{"hx-post": "/analyze", "hx-target": "#results", "hx-indicator": "#loading"}
            ),
            Div(id="loading", style="display: none; color: #666; margin: 10px 0;")("🔄 Analyzing..."),
            style="max-width: 600px; margin: 0 auto; padding: 20px;"
        ),
        Div(id="results", style="max-width: 600px; margin: 20px auto;")
    )

@app.route("/analyze", methods=["POST"])
def analyze(url: str):
    """Analyze the submitted URL and return results"""
    if not url:
        return Div(
            P("❌ Please provide a valid URL.", style="color: red;"),
            style="padding: 20px; border: 1px solid #ddd; border-radius: 5px;"
        )
    
    try:
        # Perform analysis
        analysis_results = analyze_page(url)
        
        # Format results for display
        result_items = []
        for line in analysis_results:
            if line.startswith("-"):
                result_items.append(Hr())
            elif line.strip():
                result_items.append(P(line, style="margin: 5px 0; font-family: monospace;"))
        
        return Card(
            H3(f"Analysis Results for: {url}"),
            Div(*result_items),
            Button(
                "Analyze Another URL",
                style="margin-top: 20px; padding: 8px 16px; background: #28a745; color: white; border: none; cursor: pointer;",
                **{"hx-get": "/", "hx-target": "body"}
            ),
            style="padding: 20px; border: 1px solid #ddd; border-radius: 5px; background: #f9f9f9;"
        )
        
    except Exception as e:
        return Div(
            P(f"❌ Error analyzing URL: {str(e)}", style="color: red;"),
            Button(
                "Try Again",
                style="margin-top: 10px; padding: 8px 16px; background: #007acc; color: white; border: none; cursor: pointer;",
                **{"hx-get": "/", "hx-target": "body"}
            ),
            style="padding: 20px; border: 1px solid #ddd; border-radius: 5px;"
        )

if __name__ == "__main__":
    serve()