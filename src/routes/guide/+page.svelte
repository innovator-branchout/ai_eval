<svelte:head>
	<title>How It Works</title>
	<meta
		name="description"
		content="explains how to use the model"
	/>
</svelte:head>

<main>
	<h1>How It Works</h1>

	<section id="overview">
		<h2>Overview</h2>

		<p>
			To use our model, input the prompt and responses .......
		</p>
	</section>

	<section id="index_system">
		<h2>The Index System</h2>

		<p>
			For our model, we use the index system......
		</p>
	</section>

	<section id="examples">
		<h2>Examples</h2>

		<p>
			Here are some examples of inputs and outputs to our model
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
		margin-top: 6rem;
		padding: 2rem;
		border-left: 5px solid var(--seagrass);
		border-radius: 0.5rem;
		background: var(--surface);
	}

</style>
