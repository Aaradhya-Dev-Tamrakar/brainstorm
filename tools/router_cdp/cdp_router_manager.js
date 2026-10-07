#!/usr/bin/env node
/**
 * Router CDP Management Controller
 * =====================================================================
 * Production-Grade Headful/Headless CDP Automation for Broadcom CPE / ONT
 * Supports: Automated Login, Frameset Traversal, RF Tuning, DNS Overrides,
 * Full-Page Screenshot Crawling, and Real-Time Station Auditing.
 *
 * Security Invariant: Zero credential leakage. Prompts masked via terminal stdin.
 * =====================================================================
 */

const { chromium } = require('playwright');
const readline = require('readline');
const fs = require('fs');
const path = require('path');

const BASE_DIR = __dirname;
const SCREENSHOT_DIR = path.join(BASE_DIR, 'screenshots');

function askQuestion(query) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question(query, (ans) => {
      rl.close();
      resolve(ans.trim());
    });
  });
}

function askMaskedPassword(query) {
  return new Promise((resolve) => {
    process.stdout.write(query);
    let password = '';

    if (!process.stdin.isTTY) {
      const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
      rl.question('', (ans) => { rl.close(); resolve(ans.trim()); });
      return;
    }

    process.stdin.setRawMode(true);
    process.stdin.resume();
    process.stdin.setEncoding('utf8');

    const onData = (char) => {
      if (char === '\u0003') { // Ctrl+C
        process.stdout.write('\n');
        process.exit();
      }
      if (char === '\r' || char === '\n') { // Enter
        process.stdin.setRawMode(false);
        process.stdin.pause();
        process.stdin.removeListener('data', onData);
        process.stdout.write('\n');
        resolve(password.trim());
      } else if (char === '\u0008' || char === '\u007f') { // Backspace
        if (password.length > 0) {
          password = password.slice(0, -1);
          process.stdout.write('\b \b');
        }
      } else {
        password += char;
        process.stdout.write('*');
      }
    };

    process.stdin.on('data', onData);
  });
}

const PAGES_TO_CRAWL = [
  { name: 'Device Info', url: 'info.html' },
  { name: 'Interface Statistics', url: 'statsifc.html' },
  { name: 'Optical Statistics', url: 'statsopticifc.html' },
  { name: 'DHCP Active Leases', url: 'dhcpinfo.html' },
  { name: 'Live ARP Table', url: 'arpview.cmd' },
  { name: 'Authenticated Stations', url: 'wlstationlist.cmd' },
  { name: 'Wireless Basic', url: 'wlcfg.html' },
  { name: 'Wireless Advanced RF', url: 'wlcfgadv.html' },
  { name: 'Wireless Security', url: 'wlsecurity.html' },
  { name: 'DNS Configuration', url: 'dnscfg.html' },
  { name: 'WAN Virtual Interfaces', url: 'wancfg.html' },
  { name: 'System Event Logs', url: 'logintro.html' }
];

async function runAutomatedCrawl(page, baseFrame, routerIp) {
  if (!fs.existsSync(SCREENSHOT_DIR)) {
    fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
  }

  console.log('\n[*] =========================================================');
  console.log('[*] STARTING FULL AUTOMATED PAGE CRAWL & SCREENSHOT CAPTURE');
  console.log('[*] =========================================================\n');

  const crawlResults = [];

  for (let i = 0; i < PAGES_TO_CRAWL.length; i++) {
    const item = PAGES_TO_CRAWL[i];
    const fullUrl = `http://${routerIp}/${item.url}`;
    const cleanName = item.url.replace(/\.[a-z0-9]+$/i, '');
    const shotPath = path.join(SCREENSHOT_DIR, `${String(i + 1).padStart(2, '0')}_${cleanName}.png`);

    process.stdout.write(`[*] [${i + 1}/${PAGES_TO_CRAWL.length}] Crawling ${item.name} (${item.url}) ... `);

    try {
      const target = baseFrame || page;
      await target.goto(fullUrl, { timeout: 12000, waitUntil: 'domcontentloaded' }).catch(() => {});
      await page.waitForTimeout(1000);
      await page.screenshot({ path: shotPath, fullPage: true });

      crawlResults.push({
        name: item.name,
        url: item.url,
        screenshot: path.relative(BASE_DIR, shotPath),
        status: 'SUCCESS'
      });
      console.log('DONE -> Saved screenshot');
    } catch (err) {
      console.log(`FAILED (${err.message})`);
      crawlResults.push({
        name: item.name,
        url: item.url,
        status: `ERROR: ${err.message}`
      });
    }
  }

  console.log('\n[+] =========================================================');
  console.log(`[+] CRAWL COMPLETE: ${crawlResults.length} pages captured.`);
  console.log(`[+] Screenshots stored in: ${SCREENSHOT_DIR}`);
  console.log('[+] =========================================================\n');
}

async function setWifiChannel(page, baseFrame, routerIp, targetChannel) {
  console.log(`\n[*] Automated Wi-Fi Channel Tuning -> Target Channel: ${targetChannel}`);
  const targetFrame = baseFrame || page;

  await targetFrame.goto(`http://${routerIp}/wlcfgadv.html`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1000);

  const currentVal = await targetFrame.$eval('select[name="wlChannel"]', sel => sel.value).catch(() => 'unknown');
  console.log(`[*] Current channel setting in form: ${currentVal}`);

  console.log(`[*] Setting select[name="wlChannel"] to: "${targetChannel}" ...`);
  await targetFrame.selectOption('select[name="wlChannel"]', String(targetChannel));

  console.log('[*] Submitting changes via [Apply/Save] ...');
  await targetFrame.click('input[value="Apply/Save"]');
  await page.waitForTimeout(3000);

  console.log(`[+] Wi-Fi Channel updated to Channel ${targetChannel} successfully!\n`);
}

async function setDnsServers(page, baseFrame, routerIp, primaryDns, secondaryDns) {
  console.log(`\n[*] Automated DNS Configuration -> Primary: ${primaryDns}, Secondary: ${secondaryDns}`);
  const targetFrame = baseFrame || page;

  await targetFrame.goto(`http://${routerIp}/dnscfg.html`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1000);

  const dnsRadios = await targetFrame.$$('input[name="dns"]');
  if (dnsRadios.length > 1) {
    console.log('[*] Toggling "Use Static DNS IP address" radio option...');
    await dnsRadios[1].click();
    await page.waitForTimeout(600);
  }

  console.log(`[*] Setting Primary DNS: ${primaryDns} ...`);
  await targetFrame.fill('input[name="dnsPrimary"]', primaryDns);

  if (secondaryDns) {
    console.log(`[*] Setting Secondary DNS: ${secondaryDns} ...`);
    await targetFrame.fill('input[name="dnsSecondary"]', secondaryDns);
  }

  console.log('[*] Submitting changes via [Apply/Save] ...');
  await targetFrame.click('input[value="Apply/Save"]');
  await page.waitForTimeout(3000);

  console.log('[+] DNS configuration updated successfully!\n');
}

async function main() {
  console.log('='.repeat(65));
  console.log(' BROADCOM CPE / ONT -- AUTOMATED CDP CONTROLLER');
  console.log('='.repeat(65));

  const args = process.argv.slice(2);
  const routerIp = process.env.ROUTER_IP || '192.168.1.1';
  const defaultUser = process.env.ROUTER_USER || 'user';

  const isAutoFlag = args.includes('--auto');
  const isCrawlFlag = args.includes('--crawl');
  const channelFlagIdx = args.indexOf('--set-channel');
  const targetChannelArg = channelFlagIdx !== -1 ? args[channelFlagIdx + 1] : null;

  const inputUser = await askQuestion(`Enter router username [default: ${defaultUser}]: `);
  const username = inputUser || defaultUser;

  const password = process.env.ROUTER_PASS || await askMaskedPassword(`Enter password for user [${username}]: `);

  if (!password) {
    console.error('[-] Error: Password cannot be empty.');
    process.exit(1);
  }

  console.log('[*] Initializing browser automation engine...');
  let browser;
  const launchOptions = { headless: false, slowMo: 50 };

  try {
    browser = await chromium.launch(launchOptions);
  } catch (err) {
    try {
      browser = await chromium.launch({ ...launchOptions, channel: 'chrome' });
    } catch (err2) {
      browser = await chromium.launch({ ...launchOptions, channel: 'msedge' });
    }
  }

  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();

  try {
    console.log(`[*] Connecting to http://${routerIp}/login.html ...`);
    await page.goto(`http://${routerIp}/login.html`, { timeout: 15000 });

    console.log(`[*] Authenticating as [${username}] ...`);
    await page.fill('#username', username);
    await page.fill('#password', password);
    await page.click('#loginBtn');

    await page.waitForTimeout(2500);

    const errorStatus = await page.$eval('#loginStatus', el => el.innerText).catch(() => '');
    if (errorStatus && (errorStatus.includes('Invalid') || errorStatus.includes('Wait'))) {
      console.error(`\n[-] Login failed with router message: "${errorStatus}"`);
      await browser.close();
      return;
    }

    console.log('[+] Authentication successful! Logged into management frameset.');
    const baseFrame = page.frame({ name: 'basefrm' });

    if (isAutoFlag) {
      console.log('\n[*] =========================================================');
      console.log('[*] EXECUTING FULL AUTOMATED OPTIMIZATION BUNDLE');
      console.log('[*] =========================================================\n');

      await setWifiChannel(page, baseFrame, routerIp, '6');
      await setDnsServers(page, baseFrame, routerIp, '1.1.1.1', '202.70.95.248');

      console.log('\n[+] =========================================================');
      console.log('[+] ALL AUTOMATED OPTIMIZATIONS COMPLETED SUCCESSFULLY!');
      console.log('[+] =========================================================\n');
      await browser.close();
      return;
    }

    if (isCrawlFlag) {
      await runAutomatedCrawl(page, baseFrame, routerIp);
      await browser.close();
      return;
    }

    if (targetChannelArg) {
      await setWifiChannel(page, baseFrame, routerIp, targetChannelArg);
      await browser.close();
      return;
    }

    // Interactive Menu
    let running = true;
    while (running) {
      console.log('\n' + '='.repeat(65));
      console.log(' AUTOMATED TASK MENU');
      console.log('='.repeat(65));
      console.log(' [1] Run Full Automated Page Crawl & Capture Screenshots');
      console.log(' [2] Optimize Wi-Fi Channel (Set to 1, 6, or 11)');
      console.log(' [3] Configure Fast Resilient DNS (Cloudflare + ISP)');
      console.log(' [4] View Connected Wi-Fi Stations Live (wlstationlist)');
      console.log(' [5] Keep Browser Open for Manual Exploration');
      console.log(' [6] Exit');
      console.log('='.repeat(65));

      const choice = await askQuestion('Select an option [1-6]: ');

      switch (choice) {
        case '1':
          await runAutomatedCrawl(page, baseFrame, routerIp);
          break;
        case '2': {
          const chan = await askQuestion('Enter target 2.4GHz channel (1, 6, or 11) [default: 6]: ');
          await setWifiChannel(page, baseFrame, routerIp, chan || '6');
          break;
        }
        case '3':
          await setDnsServers(page, baseFrame, routerIp, '1.1.1.1', '202.70.95.248');
          break;
        case '4': {
          const frame = baseFrame || page;
          await frame.goto(`http://${routerIp}/wlstationlist.cmd`, { waitUntil: 'domcontentloaded' });
          const text = await frame.$eval('table', t => t.innerText).catch(() => 'No table found');
          console.log('\n--- Active Wi-Fi Stations ---');
          console.log(text);
          console.log('-----------------------------\n');
          break;
        }
        case '5':
          console.log('\n[!] Browser is kept open. Press Enter in this terminal when finished.');
          await askQuestion('Press [Enter] to return to menu...');
          break;
        case '6':
        default:
          running = false;
          break;
      }
    }

    console.log('[*] Closing browser session.');
    await browser.close();

  } catch (err) {
    console.error('[-] Automation error:', err.message);
    await browser.close();
  }
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { runAutomatedCrawl, setWifiChannel, setDnsServers };
