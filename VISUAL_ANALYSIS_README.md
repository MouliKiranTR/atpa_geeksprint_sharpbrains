# Enhanced Visual Analysis System

## Overview

This enhanced onboarding agent now integrates **Figma** and **Lucid** visual content analysis with AI-powered insights. When users ask questions about designs, diagrams, or workflows, the system automatically:

1. **Searches** relevant Figma files and Lucid diagrams
2. **Captures** screenshots of visual content
3. **Analyzes** the visuals using OpenArena AI chain
4. **Provides** comprehensive, formatted responses

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

New dependencies added:
- `selenium==4.15.2` - For web automation and screenshot capture
- `Pillow==10.1.0` - For image processing

### 2. Configure API Keys

Ensure your `.env` file has:

```env
# Figma API Configuration
FIGMA_API_TOKEN=your_figma_personal_access_token_here

# Lucid API Configuration  
LUCID_API_KEY=your_lucid_api_key_here

# OpenArena Authentication (existing)
TR_ACCESS_TOKEN=your_token_here
```

### 3. Install Chrome Driver

For screenshot capture, install Chrome and ChromeDriver:

```bash
# macOS
brew install chromedriver

# Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# Windows
# Download from: https://chromedriver.chromium.org/
```

### 4. Start the Server

```bash
python run.py
```

## 📖 API Endpoints

### Enhanced Query Endpoint

**POST** `/api/v1/enhanced-query/enhanced-ask`

The main endpoint for visual analysis. Automatically detects visual queries and provides comprehensive analysis.

#### Request Body

```json
{
  "question": "Show me the design patterns in our mobile app",
  "include_figma": true,
  "include_lucid": true, 
  "include_documents": true,
  "max_visual_items": 3
}
```

#### Response

```json
{
  "success": true,
  "is_visual_query": true,
  "answer": "# Analysis Results for: Show me the design patterns...",
  "analysis_type": "design",
  "search_summary": {
    "figma_files_found": 2,
    "lucid_diagrams_found": 1,
    "documents_found": 0,
    "total_sources_searched": 3
  },
  "visual_analysis_available": true,
  "processing_time": 1.23,
  "cost": 0.0234
}
```

### Other Endpoints

- **GET** `/api/v1/enhanced-query/analysis-types` - Get available analysis types
- **GET** `/api/v1/enhanced-query/visual-keywords` - Get keywords that trigger visual analysis
- **POST** `/api/v1/enhanced-query/analyze-specific` - Analyze specific Figma/Lucid file by ID

## 🔍 How It Works

### 1. Query Analysis

The system analyzes incoming questions to determine:
- **Is it visual-related?** (contains keywords like "design", "diagram", "workflow")
- **What type of analysis?** (design, workflow, integration, or general)

```python
# Visual keywords that trigger screenshot analysis
visual_keywords = [
    "figma", "lucid", "design", "diagram", "workflow", "process",
    "visual", "interface", "ui", "ux", "chart", "flow", "mockup",
    "wireframe", "prototype", "layout", "screen", "page"
]
```

### 2. Content Search

Parallel searches across:
- **Figma Files**: Using Figma REST API
- **Lucid Diagrams**: Using Lucid REST API  
- **Uploaded Documents**: Using existing document search

### 3. Screenshot Capture

For visual content found:
- **Figma**: Uses Figma's image export API (preferred) or web screenshot fallback
- **Lucid**: Uses Lucid's export API or web screenshot fallback
- **Automatic**: Chrome headless browser for web capture

### 4. AI Analysis

Screenshots and metadata are sent to **OpenArena** with specialized prompts:

#### Analysis Types

| Type | Focus | Keywords |
|------|-------|----------|
| **Design** | UI/UX, visual hierarchy, typography, colors | design, ui, ux, interface, layout |
| **Workflow** | Process flows, decision points, user journeys | workflow, process, flow, step, procedure |
| **Integration** | Data flows, system connections, architecture | integration, api, data flow, system |
| **General** | Comprehensive overview and analysis | overview, general, explain, describe |

### 5. Response Formatting

The system creates structured, markdown-formatted responses with:
- Search summary
- Visual analysis results
- Found items details  
- Processing metadata
- Cost tracking

## 🎯 Example Usage

### Design Analysis

**Query:** "What design patterns are used in our mobile app?"

**System Response:**
1. Detects "design" keyword → triggers visual analysis
2. Searches Figma for mobile app related files
3. Captures screenshots of relevant designs
4. Analyzes with OpenArena using design-focused prompts
5. Returns detailed analysis of UI patterns, color schemes, typography

### Workflow Analysis  

**Query:** "How does the user registration process work?"

**System Response:**
1. Detects "process" keyword → triggers workflow analysis
2. Searches Lucid diagrams for registration flows
3. Captures diagram screenshots
4. Analyzes with workflow-focused prompts
5. Returns process mapping, bottlenecks, and improvements

### Integration Analysis

**Query:** "Show me the API integration architecture"

**System Response:**
1. Detects "integration" and "architecture" → triggers integration analysis
2. Searches both Figma and Lucid for architecture diagrams
3. Captures relevant visual content
4. Analyzes system connections and data flows
5. Returns technical architecture insights

## 🔧 Configuration

### Environment Variables

```env
# Required for visual analysis
FIGMA_API_TOKEN=figd_your_token_here
LUCID_API_KEY=key-your_key_here

# Screenshot capture settings (optional)
CHROME_HEADLESS=true
SCREENSHOT_QUALITY=2  # 1x or 2x scale
CAPTURE_TIMEOUT=30    # seconds

# Analysis settings (optional)  
MAX_VISUAL_ITEMS=3    # per query
ENABLE_SCREENSHOTS=true
OPENARENA_VISUAL_BUDGET=35425  # tokens
```

### Service Configuration

```python
# Custom analysis types
ANALYSIS_TYPES = {
    "design": {
        "keywords": ["design", "ui", "ux", "interface"],
        "prompt_focus": "UI/UX and visual design principles"
    },
    "workflow": {
        "keywords": ["workflow", "process", "flow"], 
        "prompt_focus": "Process flows and user journeys"
    }
    # ... more types
}
```

## 🚀 Advanced Features

### Screenshot Optimization

- **API-first**: Prefers native export APIs over web screenshots
- **Fallback mechanisms**: Web capture when APIs fail
- **Quality control**: 2x scaling for better analysis
- **Timeout handling**: Graceful failures with metadata-only analysis

### Cost Management

- **Token budgeting**: Configurable limits for OpenArena usage
- **Cost tracking**: Real-time cost reporting per query
- **Optimization**: Efficient prompting to minimize token usage

### Parallel Processing

- **Concurrent searches**: Figma, Lucid, and documents searched simultaneously
- **Async screenshot capture**: Multiple screenshots captured in parallel
- **Non-blocking**: Fast response times with async processing

## 🧪 Testing

### Run Test Suite

```bash
python test_visual_analysis.py
```

The test suite includes:
- **Query workflow simulation**
- **Individual service component tests** 
- **API endpoint structure validation**
- **Response formatting verification**

### Manual Testing

1. **Start the server**: `python run.py`
2. **Open docs**: http://localhost:8000/docs
3. **Test endpoint**: `/api/v1/enhanced-query/enhanced-ask`
4. **Try sample queries**:
   - "Show me our mobile app design patterns"
   - "What workflow is documented in our Lucid diagrams?"
   - "How does the API integration work?"

## 📊 Performance

### Typical Processing Times

| Query Type | Processing Time | Cost Range |
|------------|----------------|------------|
| **Visual Query** (with screenshots) | 3-8 seconds | $0.02-0.05 |
| **Text-only Query** | 1-3 seconds | $0.01-0.02 |
| **Document Search** | 0.5-1 seconds | $0.005-0.01 |

### Optimization Tips

1. **Limit visual items**: Use `max_visual_items` parameter
2. **Targeted searches**: Include specific keywords in queries
3. **Cache results**: Consider implementing response caching
4. **Batch processing**: Group related queries when possible

## 🔒 Security & Privacy

### Data Handling

- **Screenshots**: Processed in-memory, not stored permanently
- **API tokens**: Stored securely in environment variables
- **User queries**: Not logged or stored by default
- **Analysis results**: Temporary processing only

### Access Control

- **API rate limiting**: Implement based on your needs
- **Token validation**: Verify Figma/Lucid API access
- **User authentication**: Add as needed for your organization

## 🛠️ Troubleshooting

### Common Issues

#### "Chrome driver not found"
```bash
# Install ChromeDriver
brew install chromedriver  # macOS
sudo apt-get install chromium-chromedriver  # Ubuntu
```

#### "Figma API authentication failed"
- Verify your personal access token in `.env`
- Check token permissions in Figma settings

#### "Lucid API key invalid"  
- Confirm API key format and permissions
- Test with Lucid API documentation

#### "OpenArena authentication failed"
- Check TR_ACCESS_TOKEN in environment
- Verify token expiration and refresh if needed

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Future Enhancements

### Planned Features

1. **Real-time collaboration**: Live updates when designs change
2. **Version comparison**: Compare different versions of designs
3. **Annotation support**: Add comments and feedback to visual analysis
4. **Export options**: PDF, PowerPoint export of analysis results
5. **Advanced filtering**: Filter by teams, projects, date ranges

### Integration Opportunities

- **Slack bot**: Query visual content from Slack
- **Teams integration**: Microsoft Teams app
- **Confluence pages**: Embed analysis in documentation
- **Dashboard**: Visual analytics dashboard

## 📞 Support

For questions or issues:

1. **Check logs**: Review server logs for error details
2. **Test components**: Run `test_visual_analysis.py`
3. **API documentation**: Visit `/docs` endpoint
4. **Configuration**: Verify all environment variables

---

**🎉 Congratulations!** Your onboarding agent now has powerful visual analysis capabilities. Users can ask questions about designs and workflows, and get comprehensive AI-powered insights with visual context. 