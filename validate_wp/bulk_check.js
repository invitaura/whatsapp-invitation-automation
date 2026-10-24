import pkg from 'whatsapp-web.js';
const { Client, LocalAuth } = pkg;
import qrcode from 'qrcode-terminal';
import fs from 'fs';
import readline from 'readline';

// --- CONFIGURATION ---
const INPUT_FILE = 'numbers.txt';
const VALID_OUTPUT_FILE = 'valid_numbers.txt';
const DELAY_MS = 5000; 

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

function cleanNumber(rawNumber) {
    return rawNumber.replace(/\D/g, '');
}

async function loadNumbers(filePath) {
    const numbers = [];
    if (!fs.existsSync(filePath)) {
        console.error(`Error: File ${filePath} not found.`);
        process.exit(1);
    }
    const fileStream = fs.createReadStream(filePath);
    const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

    for await (const line of rl) {
        const trimmed = line.trim();
        if (trimmed) numbers.push(trimmed);
    }
    return numbers;
}

client.on('qr', (qr) => {
    console.log('Scan this QR code with your phone WhatsApp App:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', async () => {
    console.log('WhatsApp Client initialized. Commencing batch verification...');
    
    const rawNumbers = await loadNumbers(INPUT_FILE);
    console.log(`Loaded ${rawNumbers.length} entries from ${INPUT_FILE}.\n`);

    fs.writeFileSync(VALID_OUTPUT_FILE, '');

    for (let i = 0; i < rawNumbers.length; i++) {
        const raw = rawNumbers[i];
        const cleaned = cleanNumber(raw);

        if (!cleaned) {
            console.log(`[${i + 1}/${rawNumbers.length}] Skipped format anomalies: "${raw}"`);
            continue;
        }

        try {
            const whatsappId = `${cleaned}@c.us`;
            const isRegistered = await client.isRegisteredUser(whatsappId);

            if (isRegistered) {
                console.log(`[${i + 1}/${rawNumbers.length}] ✅ ACTIVE: ${cleaned}`);
                fs.appendFileSync(VALID_OUTPUT_FILE, `+${cleaned}\n`);
            } else {
                console.log(`[${i + 1}/${rawNumbers.length}] ❌ NON-WHATSAPP: ${cleaned}`);
            }
        } catch (error) {
            console.error(`[${i + 1}/${rawNumbers.length}] ⚠️ Check failed for ${cleaned}:`, error.message);
        }

        if (i < rawNumbers.length - 1) {
            await delay(DELAY_MS);
        }
    }

    console.log(`\nBatch checking finalized. Active records logged in: ${VALID_OUTPUT_FILE}`);
    await client.destroy();
    process.exit(0);
});

client.initialize();
