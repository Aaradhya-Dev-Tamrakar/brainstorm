import http from "http";
import url from "url";
import fs from "fs";
import path from "path";
import { exec } from "child_process";

const PORT = 58246;

const oauthPath =
  process.env.CLASSROOM_OAUTH_PATH ||
  path.join(process.env.USERPROFILE || process.env.HOME || "", ".classroom-credentials.json");

const credentialsPath =
  process.env.CLASSROOM_CREDENTIALS_PATH ||
  path.join(process.env.USERPROFILE || process.env.HOME || "", ".classroom-server-credentials.json");

const SCOPES = [
  "https://www.googleapis.com/auth/classroom.courses.readonly",
  "https://www.googleapis.com/auth/classroom.coursework.me",
  "https://www.googleapis.com/auth/classroom.coursework.students",
  "https://www.googleapis.com/auth/classroom.announcements.readonly",
  "https://www.googleapis.com/auth/classroom.rosters.readonly",
  "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",
  "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
  "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly"
];

async function main() {
  if (!fs.existsSync(oauthPath)) {
    console.error("OAuth credentials file not found at:", oauthPath);
    process.exit(1);
  }

  const oauth = JSON.parse(fs.readFileSync(oauthPath, "utf-8"));
  const keys = oauth.installed || oauth.web;

  const server = http.createServer(async (req, res) => {
    try {
      const parsedUrl = url.parse(req.url, true);
      const code = parsedUrl.query.code;
      if (code) {
        const body = new URLSearchParams({
          code: code.toString(),
          client_id: keys.client_id,
          client_secret: keys.client_secret,
          redirect_uri: `http://localhost:${PORT}`,
          grant_type: "authorization_code",
        });

        const tokenRes = await fetch("https://oauth2.googleapis.com/token", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: body.toString(),
        });

        if (!tokenRes.ok) {
          const errText = await tokenRes.text();
          res.writeHead(500, { "Content-Type": "text/html" });
          res.end(`<h1>Authentication Failed</h1><pre>${errText}</pre>`);
          console.error("Failed to exchange code for token:", errText);
          return;
        }

        const tokens = await tokenRes.json();
        fs.writeFileSync(credentialsPath, JSON.stringify(tokens, null, 2));

        res.writeHead(200, { "Content-Type": "text/html" });
        res.end(`
          <html>
            <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; text-align: center; padding: 60px; background: #0f172a; color: #f8fafc;">
              <h1 style="color: #22c55e; font-size: 28px;">Google Classroom Authentication Successful!</h1>
              <p style="font-size: 18px; margin-top: 16px;">Classroom API access tokens have been safely saved.</p>
              <p style="color: #94a3b8; font-size: 14px;">You can safely close this browser window and return to Antigravity.</p>
            </body>
          </html>
        `);
        console.log(`\nTokens successfully saved to: ${credentialsPath}`);
        setTimeout(() => {
          server.close();
          process.exit(0);
        }, 1500);
      }
    } catch (err) {
      console.error("Callback error:", err);
      res.writeHead(500, { "Content-Type": "text/plain" });
      res.end("Internal Server Error");
    }
  });

  server.listen(PORT, () => {
    const redirectUri = `http://localhost:${PORT}`;

    const authUrl = new URL("https://accounts.google.com/o/oauth2/v2/auth");
    authUrl.searchParams.set("client_id", keys.client_id);
    authUrl.searchParams.set("redirect_uri", redirectUri);
    authUrl.searchParams.set("response_type", "code");
    authUrl.searchParams.set("scope", SCOPES.join(" "));
    authUrl.searchParams.set("access_type", "offline");
    authUrl.searchParams.set("prompt", "consent");

    console.log("========================================================");
    console.log("OPENING_AUTH_URL: " + authUrl.toString());
    console.log("========================================================");

    exec(`start "" "${authUrl.toString()}"`);
  });
}

main().catch(console.error);
