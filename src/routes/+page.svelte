<svelte:head>
	<title>AI Reliability Audit</title>
	<meta
		name="description"
		content="wow"
	/>
</svelte:head>

<main>
	<h1>AI Reliability Audit</h1>

	<p>
		We're building a system to evaluate AI responses.
	</p>

	<a class="primary-button" href="#about">Learn more</a>

	<section id="about">
		<h2>About the project</h2>

		<p>
			Our project compares responses from multiple AI models and measures how accurate, reliable, and verifiable their answers are and predicts how reliable a response is based on blah blah blah...
		</p>
	</section>
</main>

<style>
	main {
		max-width: 900px;
		margin: 0 auto;
		padding: 5rem 2rem;
		font-family: Arial, sans-serif;
	}

	h1 {
		margin-bottom: 1rem;
		font-size: 3rem;
	}

	p {
		max-width: 650px;
		margin-bottom: 2rem;
		font-size: 1.1rem;
		line-height: 1.7;
	}

	.primary-button {
		display: inline-block;
		padding: 0.8rem 1.3rem;
		border-radius: 0.5rem;
		background: #3457d5;
		color: white;
		text-decoration: none;
		font-weight: bold;
	}

	.primary-button:hover {
		opacity: 0.85;
	}

	section {
		margin-top: 6rem;
	}

	h2 {
		font-size: 2rem;
	}
</style>