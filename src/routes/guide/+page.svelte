<svelte:head>
	<title>How It Works</title>
	<meta
		name="description"
		content="explains how to use the model"
	/>
</svelte:head>

<main>
	<h1>Use Guide</h1>

    <p>
		Understanding how to use the AI Reliability Audit.
	</p>

	<section id="overview">
		<h2>Overview</h2>

		<p>
			To use our model, input the prompt and responses of a LLM into their respective textboxes, then click the evalulate button. Our model will then predict the score of the LLM, measuring its accuracy, reliability, and credibility.
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

		<h3>Example 1</h3>

		<p>
			Prompt: .... <br>
			Response: ... <br>
			Score: ....
		</p>

		<h3>Example 2</h3>

		<p>
			Prompt: .... <br>
			Response: ... <br>
			Score: ....
		</p>

		<h3>Example 3</h3>

		<p>
			Prompt: .... <br>
			Response: ... <br>
			Score: ....
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
		font-size: clamp(2.5rem, 8vw, 4rem);
		line-height: 1;
		letter-spacing: -0.05em;
	}

	h2 {
		margin-bottom: 1rem;
		color: var(--charcoal);
		font-size: 2rem;
	}
    h3 {
        margin-bottom: 1rem;
        color: var(--charcoal);
        font_size: 1.4rem;
    }
	p {
		max-width: 650px;
		margin-bottom: 2rem;
		color: var(--muted);
		font-size: 1.1rem;
		line-height: 1.7;
	}
    section {
		margin-top: 2rem;
		padding: 2rem;
		border-left: 5px solid var(--seagrass);
		border-radius: 0.5rem;
		background: var(--surface);
	}

</style>
