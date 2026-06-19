#!/usr/bin/env node
'use strict';

const { spawn } = require('child_process');
const path = require('path');

const electron = require('electron');
const appDir = path.join(__dirname, '..');

const child = spawn(electron, [appDir], {
  stdio: 'inherit',
  env: process.env,
});

child.on('exit', (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
    return;
  }
  process.exit(code ?? 0);
});
