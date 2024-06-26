﻿# Light Linking Data Exporter And Importer

I've written this script for a friend who needed to, as the title suggests, export and import light linking data between scenes.

## Usage

### Export LLD

1. Paste the contents of (or drag and drop) `lightLinkingData-ExportImport.py` into the script editor
2. Run it and click the `Export` button

This will create a new file in the folder your scene is in, called `<sceneFileName>-lightLinkingData.pkl`.
This file holds all the LLD.

### Import LLD

1. Import or reference in the scene you've exported the LLD from into your current one
2. Paste the contents of (or drag and drop) `lightLinkingData-ExportImport.py` into the script editor
3. Run it and click the `Import` button
4. Select the `.pkl` file you've created in the [Export LLD](#export-lld) section

With this done you should now have your LLD settings imported into your current scene

## NOTE
Please don't import `.pkl` files you get from untrusted sources (e.g.: sent to you by someone else you don't trust) as they can be a security risk.
The ones created by this code are safe to use of course; you can check out (the fairly well commented) code in `lightLinkingData-ExportImport.py` to see for yourself.
