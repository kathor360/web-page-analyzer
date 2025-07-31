# 🔍 FastHTML Web Page Analyzer

A comprehensive web page analysis tool built with FastHTML that evaluates website performance, SEO optimization, accessibility, and provides actionable optimization recommendations.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastHTML](https://img.shields.io/badge/FastHTML-latest-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

### 📊 Performance Analysis
- **Page Load Time Measurement** - Real-time loading speed analysis
- **Resource Size Tracking** - HTML, CSS, JS, and image size analysis
- **Performance Grading** - A-D grades based on speed and optimization
- **Total Page Weight** - Complete resource footprint calculation

### 🔍 SEO Analysis
- **H1 Tag Validation** - Ensures proper heading structure
- **Meta Description Check** - Validates presence and optimal length (120-160 chars)
- **Title Tag Analysis** - Checks length and presence (30-60 chars optimal)
- **Canonical Tag Detection** - Identifies duplicate content prevention

### 📁 Resource Optimization
- **CSS File Analysis** - Counts stylesheets and suggests combining
- **JavaScript Bundling Recommendations** - Identifies JS optimization opportunities
- **External Dependency Tracking** - Monitors third-party resource usage
- **File Listing** - Complete inventory of all CSS and JS files

### 🖼️ Image Optimization
- **Alt Text Validation** - Accessibility compliance checking
- **Image Size Analysis** - Identifies oversized images (>200KB)
- **Modern Format Suggestions** - Recommends WebP/AVIF conversion
- **Lazy Loading Recommendations** - Performance improvement suggestions

### 🚀 Smart Recommendations
- **Performance Optimization** - GZIP, CDN, minification suggestions
- **Resource Bundling** - CSS/JS combination recommendations
- **Caching Strategies** - Browser caching optimization
- **Modern Web Standards** - WebP images, resource hints, preloading

### ♿ Accessibility Features
- **Interactive Element Analysis** - onclick button detection
- **Image Alt Text Validation** - Screen reader compatibility
- **Semantic HTML Checking** - Proper heading structure validation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project files**
2. **Install dependencies:**
   ```bash
   pip install fasthtml beautifulsoup4 requests pillow
   ```

3. **Run the application:**
   ```bash
   python analyzer.py
   ```

4. **Open your browser** to the displayed URL (typically `http://localhost:5001`)

### Usage

1. Enter any website URL in the input field
2. Click "Analyze Page" 
3. View comprehensive analysis results including:
   - Performance metrics and grading
   - SEO optimization status
   - Resource breakdown and recommendations
   - Image optimization opportunities
   - Accessibility compliance

## 📊 Performance Grading System

| Grade | Load Time | Page Size | Description |
|-------|----------|-----------|-------------|
| 🏆 **A** | < 1.0s | < 500KB | Excellent |
| 🥈 **B** | < 2.0s | < 1MB | Good |
| 🥉 **C** | < 3.0s | < 2MB | Needs Improvement |
| 🚨 **D** | > 3.0s | > 2MB | Poor - Requires Optimization |

## 🛠️ Technical Architecture

### Built With
- **[FastHTML](https://fastht.ml/)** - Python web framework with HTMX integration
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** - HTML parsing and analysis
- **[Requests](https://requests.readthedocs.io/)** - HTTP library for web scraping
- **[Pillow](https://pillow.readthedocs.io/)** - Image processing and analysis

### Key Components
- **FastHTML Routes** - Clean URL routing and request handling
- **HTMX Integration** - Seamless form submission without page refresh
- **Responsive Design** - Mobile-friendly interface using Pico CSS
- **Real-time Analysis** - Live performance measurement and reporting

## 📝 Sample Analysis Output

```
📊 PERFORMANCE METRICS
⏱️ Page Load Time: 1.23 seconds
📦 HTML Size: 45.2 KB
✅ FAST: Good page load time

🔍 SEO ANALYSIS
✅ Exactly one <h1> tag found.
✅ Meta description present (142 chars).
✅ Title tag present (48 chars).
❌ Canonical tag missing.

📁 RESOURCE ANALYSIS
🎨 CSS Files: 3
📜 JavaScript Files Found:
   1. https://code.jquery.com/jquery-3.6.0.min.js
   2. https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js
   3. /assets/js/app.js

🚀 OPTIMIZATION RECOMMENDATIONS
📦 Minify HTML, CSS, and JavaScript
🖼️ Optimize images (compress, resize, use WebP)
💾 Set proper browser caching headers
🔧 Use resource hints (dns-prefetch, preconnect)

🏆 Performance Grade: B - Good
```

## 🔧 Customization

### Adding New Analysis Features

1. **Extend the `analyze_page()` function:**
   ```python
   def analyze_page(url):
       # Add your custom analysis logic
       result.append("🆕 Your new analysis feature")
   ```

2. **Add new recommendation logic:**
   ```python
   if your_condition:
       recommendations.append("💡 Your optimization suggestion")
   ```

### Modifying Performance Thresholds

Update the grading criteria in the analysis function:
```python
if load_time < 1.0 and total_size < 500:
    result.append("🏆 Performance Grade: A - Excellent")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**ImportError with FastHTML:**
```bash
pip install --upgrade fasthtml
```

**403 Forbidden Errors:**
- The analyzer includes proper User-Agent headers to avoid most blocking
- Some websites may still block automated requests
- Try accessing the URL manually first to verify it's accessible

**Timeout Errors:**
- Default timeout is 10 seconds
- Slow websites may need longer timeout values
- Check your internet connection

### Performance Tips

- **Large websites** may take longer to analyze due to image checking
- **Image analysis** can be disabled for faster results if needed
- **External resources** may slow down analysis on sites with many third-party dependencies

## 🙋‍♀️ Support

If you encounter issues or have questions:
1. Check the troubleshooting section above
2. Review the FastHTML documentation at [fastht.ml](https://fastht.ml)
3. Open an issue with detailed error information

## 🎯 Roadmap

- [ ] Lighthouse score integration
- [ ] Core Web Vitals measurement
- [ ] PDF report generation
- [ ] Batch URL analysis
- [ ] Historical performance tracking
- [ ] Mobile vs Desktop analysis
- [ ] Security header analysis
- [ ] Carbon footprint calculation

---

**Made with ❤️ using FastHTML** | **Perfect for web developers, SEO specialists, and site auditors**
