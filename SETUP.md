# 🚀 Quick Setup Guide

Get your AI Research Collaborator running in 5 minutes!

## Step 1: Get Your Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

## Step 2: Set Environment Variable

### Windows PowerShell
```powershell
$env:GOOGLE_API_KEY="paste-your-api-key-here"
```

### Linux/Mac
```bash
export GOOGLE_API_KEY="paste-your-api-key-here"
```

### Or Create .env File (Recommended)
```bash
# Copy template
cp .env.template .env

# Edit .env file and add:
GOOGLE_API_KEY=your-actual-api-key-here
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected packages:
- `google-genai>=1.0.0`
- `python-dotenv>=1.0.0`
- `requests>=2.31.0`

## Step 4: Run Demo

Test that everything works:

```bash
python demo.py
```

You should see:
- ✅ API Key found!
- 🔬 Running Quick Research Demo...
- Research results appear

## Step 5: Try Examples

Run the main application:

```bash
python main.py
```

Choose an option:
1. **Quick Research** - Fast, 3 sources (~5 min)
2. **Deep Research** - Comprehensive with report (~20 min)
3. **Comparative Research** - Compare multiple topics
4. **Custom Workflow** - Build your own workflow
5. **Memory Retrieval** - View past research
6. **Interactive Mode** - Full interactive experience ⭐

## Troubleshooting

### "GOOGLE_API_KEY not set"
- Check: `echo $env:GOOGLE_API_KEY` (Windows) or `echo $GOOGLE_API_KEY` (Linux/Mac)
- Solution: Set the environment variable again

### "Module not found"
- Solution: Run `pip install -r requirements.txt`
- Check: `pip list | grep google-genai`

### "API Error" or "Rate Limit"
- Check: API key is valid at [Google AI Studio](https://aistudio.google.com/app/apikey)
- Wait a minute and try again (rate limits)

### "Import Error"
- Make sure you're in the project directory
- Check: `pwd` should show `.../kaggle-agent-project`

## Next Steps

1. ✅ **Complete** - You're ready to use the system!
2. 📖 **Learn More** - Read `README.md` for detailed documentation
3. 🎯 **Use It** - Start researching your topics
4. 🎓 **Submit** - For Kaggle Capstone submission

## Quick Reference

### File Structure
```
kaggle-agent-project/
├── agents/              # All agent code
├── config/              # Configuration
├── main.py             # Main app (run this)
├── demo.py             # Quick demo
├── memory_manager.py   # Memory system
├── README.md           # Full documentation
└── requirements.txt    # Dependencies
```

### Key Commands

```bash
# Quick test
python demo.py

# Main application
python main.py

# Interactive mode (best experience)
python main.py
# Then select option 6
```

### Usage Example

```python
from agents import OrchestratorAgent

orchestrator = OrchestratorAgent()
results = orchestrator.quick_research("Your topic here")
print(results)
```

## Support

- 📖 Read `README.md` for comprehensive guide
- 🐛 Check Troubleshooting section above
- 💬 Ask on Kaggle Discord for Capstone help

---

**You're all set! Happy researching! 🎓✨**
