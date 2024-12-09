import fontAwesomeIconGenerator from 'font-awesome-icon-generator'
import favicons from "favicons";
import fs from "fs/promises";

const staticDir='../src/pmorch_gallery/renderers/static'

const config = {
  iconOutputFile: (size) => `${staticDir}/gallery-${size}.png`,
  unicodeHex: 'f009',
  color: '#4287f5',
  sizes: [32, 512],
}

await fontAwesomeIconGenerator(config)

const src = `${staticDir}/gallery-512.png`;
const faviconFileName = `${staticDir}/favicon.ico`
const faviconName = `favicon.ico`

const response = await favicons(src, { path: "/never-used-but-needs-a-value"});
const faviconImage = response.images.filter(i => i.name == faviconName)[0]
await fs.writeFile(faviconFileName, faviconImage.contents)
