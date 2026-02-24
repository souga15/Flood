# 🌐 How to Access Your Flood Risk Dashboard

## Quick Access

Your application has **2 parts running**:

### 1. Backend API ✅
- **URL**: http://localhost:5000
- **Status**: Running
- **Test**: Visit http://localhost:5000 in browser - you should see API docs

### 2. Frontend Dashboard 🖥️
- **Typical URL**: http://localhost:5173
- **Alternative**: http://localhost:5174 (if 5173 is taken)

## How to Find Your Frontend URL

Look at your **frontend terminal** (the one running `npm run dev`). 

You should see output like:
```
  VITE v5.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.x.x:5173/
```

The **Local** URL is what you need!

## If You Don't See the URL

### Option 1: Check the terminal running `npm run dev`
The URL is printed when Vite starts. Scroll up in that terminal window.

### Option 2: Try common ports
Open these URLs in your browser:
- http://localhost:5173
- http://localhost:5174
- http://localhost:3000

### Option 3: Restart frontend
```bash
# Stop the current frontend (Ctrl+C in terminal)
cd C:\Users\souga\OneDrive\Desktop\FloodRiskPredictor\frontend
npm run dev
```

The URL will be printed when it starts.

## What You Should See

Once you access the frontend URL, you'll see:
- ✅ Flood Risk Dashboard header
- ✅ City selector dropdown
- ✅ "Refresh Data" button
- ✅ Map view on the right

## Test It's Working

1. Select **"Patna"** from dropdown
2. Click **"Refresh Data"**
3. You should see:
   - Weather Display (temp, rainfall, windspeed)
   - Flood Risk Indicator (Low/Moderate/High/Severe)
   - **NEW**: "What's Influencing This Prediction?" panel
   - Map with location pin

## Troubleshooting

**"Cannot reach site" error?**
- Make sure frontend terminal says "ready" (not still installing)
- Try http://127.0.0.1:5173 instead of localhost
- Check Windows Firewall isn't blocking

**See old version without new features?**
- Hard refresh: Ctrl+Shift+R
- Or clear browser cache

**Frontend won't start?**
```bash
cd C:\Users\souga\OneDrive\Desktop\FloodRiskPredictor\frontend
npm install  # Reinstall dependencies
npm run dev
```
