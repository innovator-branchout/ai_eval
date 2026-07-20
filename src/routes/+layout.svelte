<script>
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<nav>
	<a href="/">Home</a>
	<a href="/test">test</a>
</nav>

{@render children()}

<style>
	nav {
		display: flex;
		gap: 1rem;
		padding: 1rem;
		border-bottom: 1px solid #ccc;
	}

	nav a {
		color: inherit;
		text-decoration: none;
	}

	nav a:hover {
		text-decoration: underline;
	}
</style>
