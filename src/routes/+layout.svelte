<script>
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<nav>
	<a href="/">Home</a>
	<a href="/guide">How it works</a>
	<a href="/model">Model</a>
	<a href="/about">About</a>
	<a href="/contact">Contact</a>
</nav>

{@render children()}

<style>
	nav {
		display: flex;
		gap: 2rem;
		padding: 1.25rem 2rem;
		background: var(--charcoal);
	}

	nav a {
		color: white;
		font-weight: 600;
		text-decoration: none;
	}

	nav a:hover {
		color: var(--seagrass);
	}
</style>