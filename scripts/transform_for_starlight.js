import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SOURCE_DIRS = ['docs', 'docs_zh'];
const OUTPUT_DIR = path.join(__dirname, '../dist-starlight');

// Ensure output directory exists
if (fs.existsSync(OUTPUT_DIR)) {
    fs.rmSync(OUTPUT_DIR, { recursive: true, force: true });
}
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

function transformContent(content) {
    // 1. Transform GitHub Alerts to Starlight Asides
    // > [!NOTE] -> :::note
    // > [!TIP] -> :::tip
    // > [!IMPORTANT] -> :::caution
    // > [!WARNING] -> :::caution
    // > [!CAUTION] -> :::danger
    
    const alertMap = {
        'NOTE': 'note',
        'TIP': 'tip',
        'IMPORTANT': 'caution',
        'WARNING': 'caution',
        'CAUTION': 'danger'
    };

    let transformed = content.replace(/^> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\n((?:> .*\n?)*)/gm, (match, type, body) => {
        const starlightType = alertMap[type] || 'note';
        const cleanBody = body.replace(/^> /gm, '');
        return `:::${starlightType}\n${cleanBody}:::\n`;
    });

    return transformed;
}

function processFile(filePath, relativePath) {
    let content = fs.readFileSync(filePath, 'utf-8');
    
    // Add frontmatter if missing
    if (!content.startsWith('---')) {
        const fileName = path.basename(filePath, '.md');
        const title = fileName.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        content = `---\ntitle: ${title}\n---\n\n${content}`;
    }

    content = transformContent(content);

    const outputPath = path.join(OUTPUT_DIR, relativePath);
    const outputDir = path.dirname(outputPath);
    
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    fs.writeFileSync(outputPath, content);
    console.log(`Processed: ${relativePath}`);
}

function walkDir(dir, baseDir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat.isDirectory()) {
            walkDir(filePath, baseDir);
        } else if (file.endsWith('.md')) {
            const relativePath = path.relative(path.join(__dirname, '..'), filePath);
            // Adjust path structure for Starlight if needed
            // For now, we keep docs/ and docs_zh/ as is, but maybe we want to map them to src/content/docs/mythicprefixes/en and .../zh
            // Let's assume the consumer will map 'docs' to 'en' and 'docs_zh' to 'zh' or similar.
            // Or we can do it here.
            
            let targetPath = relativePath;
            if (relativePath.startsWith('docs\\') || relativePath.startsWith('docs/')) {
                 targetPath = relativePath.replace(/^docs[\\/]/, 'en/');
            } else if (relativePath.startsWith('docs_zh\\') || relativePath.startsWith('docs_zh/')) {
                 targetPath = relativePath.replace(/^docs_zh[\\/]/, 'zh/');
            }
            
            processFile(filePath, targetPath);
        }
    }
}

SOURCE_DIRS.forEach(dir => {
    const fullPath = path.join(__dirname, '..', dir);
    if (fs.existsSync(fullPath)) {
        walkDir(fullPath, fullPath);
    }
});

console.log('Transformation complete.');
