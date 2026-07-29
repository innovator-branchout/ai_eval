<script>
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import logo from '$lib/assets/logo.png';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<nav>
	<a class="logo-link" href="/" aria-label="Home">
		<img class="logo" src={logo} alt="AI Reliability Audit" />
	</a>
	<a class="nav-link" href="/guide">Guide</a>
	<a class="nav-link" href="/model">Model</a>
	<a class="nav-link" href="/about">About</a>

</nav>

{@render children()}

<style>
	nav {
		display: flex;
		align-items: center;
		gap: 2rem;
		padding: 0 2rem;
		background: var(--charcoal);
	}

	.nav-link {
		padding: 1.25rem 0;
		color: white;
		font-weight: 600;
		text-decoration: none;
	}

	.nav-link:hover {
		color: var(--seagrass);
	}

	.logo-link {
		display: flex;
		align-items: center;
		margin-right: 0.5rem;
		text-decoration: none;
	}

	.logo-link:hover {
		opacity: 0.85;
	}

	.logo {
		display: block;
		height: 2rem;
		width: auto;
	}
</style>
