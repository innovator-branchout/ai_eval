<script>
    let prompt = $state('');
    let response = $state('');
</script>

<svelte:head>
	<title>Model</title>
	<meta
		name="description"
		content="Model page"
	/>
</svelte:head>

<main>
	<h1>Model</h1>

	<p>
		Test out our model to evalulate responses from various AI models!
	</p>

	<section>
        <p>
            If you haven't already, we highly recommend reading the <a href="/guide">"Guide"</a> page to learn more about using our model!
        </p>
	</section>

	<section>
        <h2> Test It Out! </h2>
        <p>Enter the prompt and response to the model, then click the "Evalulate" button to get its score.</p>

        <br>

        <h3>Enter your prompt: </h3>
        <input type="prompt" bind:value={prompt} placeholder="What did you ask?"/>
        <br>
        <h3>Enter the response: </h3>
        <input type="response" bind:value={response} placeholder="What did the model say?"/>

        <br>
        <br>
        <br>

        <a class="primary-button" href="/model">Evalulate</a>

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

	h3 {
        margin-bottom: 1rem;
        color: var(--charcoal);
        font-size: 1.1rem;
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

	.primary-button {
		display: inline-block;
		padding: 0.8rem 1.3rem;
		border-radius: 0.5rem;
		background: var(--wine);
		color: white;
		font-weight: bold;
		text-decoration: none;
	}

	.primary-button:hover {
		background: #591716;
	}

	input {
        max-width: 650px;
		margin-bottom: 2rem;
		color: var(--charcoal);
		font-size: 1.1rem;
		line-height: 1.7;
		border-radius: 8px;
	}
</style>
