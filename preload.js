const { contextBridge } = require('electron');

// Nothing privileged is needed in the renderer (the rain is pure canvas),
// so the bridge stays intentionally small.
contextBridge.exposeInMainWorld('caffeinatrix', {
  version: process.versions.electron,
});
