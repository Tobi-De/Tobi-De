---
share: true
featured: true
title: >
   Maximizing Productivity: PyCharm and htmx Integration
slug: maximizing-productivity-pycharm-and-htmx-integration
tags:
 - django
 - htmx
 - pycharm
description: Throughout this quick guide, we will see how to add htmx support (documentation and autocompletion) in pycharm.
publish_date: 2022-11-05
upload_path: posts
---

> **TL;DR** Learn how to add support for htmx in PyCharm for seamless development using [web-types](https://github.com/JetBrains/web-types#web-types).

If you're not familiar with htmx, check out this fantastic [htmx + Django introduction](https://www.youtube.com/watch?v=Ula0c_rZ6gk) by [BugBytes](https://www.bugbytes.io/).

### Introduction

[htmx](https://htmx.org/) is my go-to frontend tool for building web applications, and [PyCharm from JetBrains](https://www.jetbrains.com/pycharm/) is my daily code editor/IDE. Unfortunately, by default, PyCharm doesn't recognize htmx attributes when used in templates, resulting in ugly warning lines 🙁.  This article will guide you on how to resolve this issue and improve your development workflow.

### The Fix

There's a simple way to add autocompletion and documentation for htmx attributes in JetBrains editors using [web-types](https://github.com/JetBrains/web-types#web-types). Web-types is a JSON-based format that provides IDEs with metadata information about web component libraries like htmx. I stumbled upon this tip via [this tweet](https://twitter.com/sponsfreixes/status/1573725414643535872), so kudos to the author for sharing it!

### Step-by-Step Guide

 - **Create a `package.json` File**

   Start by creating a `package.json` file, the central configuration file for Node.js-based applications. Although we're not building a Node.js package, this is the method to reference web-types in your PyCharm project. Ensure you have Node.js installed on your computer. If not, I recommend using [nvm](https://github.com/nvm-sh/nvm) to install it. After installing Node.js, you can use `npm` (included with all Node.js installations) to initialize a Node.js project and generate the `package.json` file.

   ```sh
   npm init -y
   ```

- **Create `htmx.web-types.json` File**

   Create a new file named `htmx.web-types.json` and copy the htmx [web-types source](https://github.com/bigskysoftware/htmx/blob/master/editors/jetbrains/htmx.web-types.json) into it:

   ```sh
   touch htmx.web-types.json
   ```

- **Update `package.json`**

   Add a new entry to your `package.json` with "web-types" as the key and the path to your `htmx.web-types.json` file as the value. Here's an example:

   ```json
   {
     "web-types": "./htmx.web-types.json"
   }
   ```

- **Enjoy Autocompletion and Documentation**

   Now, in your HTML templates, type an htmx attribute like `hx-get`, and you should see autocompletion and documentation directly accessible in your IDE. Cool, right? 😎

### Conclusion

With this simple setup, you can enhance your PyCharm experience and work seamlessly with htmx attributes in your Django projects. Happy coding!
