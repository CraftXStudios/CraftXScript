// Cloudflare Worker Script (worker.js)
// This script intercepts incoming traffic. If the traffic is a Roblox executor, 
// it serves the Lua script. Otherwise, it serves the HTML website.

export default {
  async fetch(request, env, ctx) {
    const userAgent = request.headers.get("User-Agent") || "";
    
    // Check if the request is coming from a Roblox executor
    const isRoblox = userAgent.toLowerCase().includes("roblox") || 
                     userAgent.toLowerCase().includes("xeno") || 
                     userAgent.toLowerCase().includes("synapse") || 
                     userAgent.toLowerCase().includes("krnl") || 
                     userAgent.toLowerCase().includes("fluxus");

    if (isRoblox) {
      // 1. If it's a Roblox Executor, serve the raw Lua script.
      // You will need to host your CraftXNightScript.lua somewhere (like Github or Pastebin)
      // and paste the RAW URL here.
      const luaScriptUrl = "https://raw.githubusercontent.com/YOUR_GITHUB_NAME/YOUR_REPO/main/CraftXNightScript.lua"; 
      
      const scriptResponse = await fetch(luaScriptUrl);
      const luaCode = await scriptResponse.text();
      
      return new Response(luaCode, {
        headers: { "Content-Type": "text/plain" }
      });
    } else {
      // 2. If it's a normal web browser, serve the HTML website.
      // Assuming you upload your index.html to Cloudflare Pages or Github Pages, 
      // you can fetch the raw HTML or let the platform serve it naturally.
      
      // If you are using Cloudflare Pages, you might not even need this fetch, 
      // you can just return env.ASSETS.fetch(request)
      const htmlUrl = "https://raw.githubusercontent.com/YOUR_GITHUB_NAME/YOUR_REPO/main/index.html"; 
      
      const htmlResponse = await fetch(htmlUrl);
      const htmlContent = await htmlResponse.text();
      
      return new Response(htmlContent, {
        headers: { "Content-Type": "text/html;charset=UTF-8" }
      });
    }
  }
};
