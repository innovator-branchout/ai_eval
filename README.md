# sv

Everything you need to build a Svelte project, powered by [`sv`](https://github.com/sveltejs/cli).

## Installing Dependencies 

1. Node.js - you can just install this via the nodejs website, nodejs.org
2. npm & npv - comes with the Node.js package
3. vite
```sh
npm install -D vite
```

To test if node, npm, npx is installed correctly

```sh
# check node
node -v

#or check npm
npm -v

#or check npx
npx -v
```

Note: in order to run local scripts like npm & npv on Windows, you need to enable RemoteSigned

```sh
# enable local scripts
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Creating a project

If you're seeing this, you've probably already done this step. Congrats!

```sh
# create a new project
npx sv create my-app
```

To recreate this project with the same configuration:

```sh
# recreate this project
npx sv@0.16.3 create --template minimal --types jsdoc --install npm .
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```sh
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```sh
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.
