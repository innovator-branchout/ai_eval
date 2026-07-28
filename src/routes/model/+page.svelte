<script>
    let prompt = $state('');
    let response = $state('');

    function getScore(){
        alert('You got your score! (jk you did not this is placeholder)');
    }

    const models = [
        {model_type: "Auto", index: 1},
        {model_type: "Response", index: 2},
        {model_type: "Prompt", index: 3}
    ]

    let selectedId = $state(1);
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
            <strong>Note:</strong> If you haven't already, we highly recommend reading the <a href="/guide">"Guide"</a> page to learn more about using our model!
        </p>
	</section>

	<section>
        <h2> Test It Out! </h2>
        <p>Enter the prompt and/or response to the model, then click the "Evalulate" button to get its score. Change the dropdown if you want to select a specific model</p>

        <select bind:value={selectedId}>
            {#each models as model}
                <option value={model.index}>{model.model_type}</option>
            {/each}
        </select>

        <h3>Enter your prompt: </h3>
        <textarea type="prompt" bind:value={prompt} placeholder="What did you ask?"/>
        <br>
        <h3>Enter the response(optional): </h3>
        <textarea type="response" bind:value={response} placeholder="What did the model say?"/>


        <h3> Reliability Index: N/A</h3>

        <button onclick={getScore}>
            Evalulate
        </button>



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
		border-left: 5px solid var(--muted);
		margin-top: 2rem;
		margin-bottom: 2rem;
	}

	button {
		display: inline-block;
		padding: 0.8rem 1.3rem;
		border-radius: 0.5rem;
		background: var(--wine);
		color: white;
		font-weight: bold;
		text-decoration: none;
	}

	button:hover {
		background: #591716;
	}

	textarea {
        max-width: 650px;
		margin-bottom: 2rem;
		color: var(--charcoal);
		font-size: 1.1rem;
		line-height: 1.7;
		border-radius: 8px;
		width: 100%;
		height: 400px;
		white-space: pre-wrap;
        resize: vertical;
	}
	textarea:first-of-type {
		height: 150px;
	}
	select {
        width: 40%;
        padding: 1rem;
        border-radius:6px;

        font-family: Arial, sans-serif;
        font-weight: 600;
        color: var(--charcoal);
        font-size: 1rem;
    }
    option {
        font-family: Arial, sans-serif;
        color: var(--charcoal);
        font-size: 1rem;
        font-weight: 600;
    }
</style>
