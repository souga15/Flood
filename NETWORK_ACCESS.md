# 📱 How to Access From Other Devices

## ✅ Configuration Complete
I have configured your app for network access:
1. **Frontend**: Now listens on all network interfaces (`--host` flag)
2. **API Connection**: Updated to use your local IP (`10.151.56.191`) instead of `localhost`

## 🚀 How to Connect

### 1. Restart Frontend
You must restart the frontend terminal for changes to take effect:
```bash
# In the frontend terminal
Ctrl+C  (to stop)
npm run dev
```

### 2. Get the URL
Look at the terminal output. It will show a **Network** URL, likely:
```
  ➜  Network: http://10.151.56.191:3001/
```

### 3. Open on Mobile/Tablet
1. Ensure your phone is on the **same Wi-Fi** as your PC.
2. Open Chrome/Safari on your phone.
3. Type the Network URL (e.g., `http://10.151.56.191:3001`).

## ⚠️ Troubleshooting

**If the site doesn't load on your phone:**

### 1. Check Firewall (Most Common Issue)
Windows Firewall often blocks connections.
**Quick Test**: Temporarily disable firewall to confirm.
**Permanent Fix**: Allow "Node.js" and "Python" through Windows Firewall.

### 2. Check Backend Access
Try opening the API on your phone:
`http://10.151.56.191:5000`
- If this works (you see API docs), backend is good.
- If this fails, firewall is blocking port 5000.

### 3. Check IP Address
If `10.151.56.191` doesn't work, your IP might have changed.
Run `ipconfig` in terminal to get the current IPv4 address.
