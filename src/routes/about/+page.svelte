<svelte:head>
	<title>About</title>
	<meta
		name="description"
		content="About page."
	/>
</svelte:head>

<main>
	<h1>About</h1>

	<p>
		Our project compares responses from multiple AI models and measures how accurate, reliable, and verifiable their answers are. 
	</p>

	<section>
		<h2>Development team</h2>

		<p>
			BranchOut! Innovator
		</p>
	</section>

	<section id="contact">
		<h2>Contact</h2>

		<p>
			<a href="https://www.velbranchout.org">www.velbranchout.org</a>
		</p>

		<h2>Email us at</h2>
		<p>
			<a href="mailto:team@velbranchout.org">team@velbranchout.org</a>
		</p>
	</section>
</main>

<style>
	main {
		max-width: 900px;
		min-height: calc(100vh - 70px);
		margin: 0 auto;
		padding: 6rem 2rem;
	}

	h1 {
		margin: 0 0 1.25rem;
		color: var(--charcoal);
		font-size: clamp(3rem, 8vw, 5.5rem);
		line-height: 1;
		letter-spacing: -0.05em;
	}

	h2 {
		margin-bottom: 1rem;
		color: var(--charcoal);
		font-size: 2rem;
	}

	p {
		max-width: 650px;
		margin-bottom: 2rem;
		color: var(--muted);
		font-size: 1.1rem;
		line-height: 1.7;
	}

	section {
		margin-top: 3rem;
		padding: 2rem;
		border-left: 5px solid var(--seagrass);
		border-radius: 0.5rem;
		background: var(--surface);
	}

	section:first-of-type {
		margin-top: 4rem;
	}
</style>
