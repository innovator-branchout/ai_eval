<svelte:head>
	<title>AI Reliability Audit</title>
	<meta
		name="description"
		content="A student-built project that evaluates the reliability of AI responses."
	/>
</svelte:head>

<main>
	<section class="hero">
		<div class="hero-text">
			<h1>AI Reliability Audit</h1>

			<p class="intro">
			Our project evaluates responses from multiple AI models for accuracy, reliability, and verifiability, using our independently designed benchmark and grading system to predict the reliability of new responses.
			</p>

			<div class="buttons">
				<a class="primary-button" href="/model">Try the model</a>
				<a class="secondary-button" href="/guide">View the guide</a>
			</div>
		</div>

		<div class="hero-card">
			<h2>How it works</h2>

			<ol>
				<li>Input a prompt and response</li>
				<li>Response is evaluated by our internal neural network</li>
				<li>Receive its reliability score</li>
			</ol>
		</div>
	</section>

	<section class="about-section">
		<div>
			<p class="eyebrow">About the project</p>
			<h2>Making AI evaluation easier to understand</h2>
		</div>

		<p>
			Our project compares AI responses across categories including hallucination, bias, reasoning, citation reliability, and responsible behavior.
		</p>
	</section>

	<section class="cards">
		<article>
			<h3>Benchmark</h3>
			<p>
				Prompts created designed to test common strengths and weaknesses of AI systems
			</p>
		</article>

		<article>
			<h3>Human Evaluation</h3>
			<p>
				Reviewers score responses using a consistent grading rubric
			</p>
		</article>

		<article>
			<h3>Prediction Model</h3>
			<p>
				Our model then uses the collected data to predict how reliable a new response may be
			</p>
		</article>
	</section>

	<section class="callout">
		<div>
			<h2>See in action</h2>
			<p>Enter a prompt and AI response to receive an evaluation</p>
		</div>

		<a class="primary-button" href="/model">Go to Model</a>
	</section>
</main>

<style>
	main {
		max-width: 1100px;
		margin: 0 auto;
		padding: 5rem 2rem;
	}

	.hero {
		display: grid;
		grid-template-columns: 1.3fr 0.7fr;
		gap: 4rem;
		align-items: center;
		min-height: 500px;
	}

	.eyebrow {
		margin-bottom: 1rem;
		color: var(--seagrass);
		font-size: 0.85rem;
		font-weight: 700;
		letter-spacing: 0.12em;
		text-transform: uppercase;
	}

	h1 {
		max-width: 500px;
		margin: 0 0 1.5rem;
		font-size: clamp(2.5rem, 6vw, 6rem);
		line-height: 0.95;
		letter-spacing: -0.06em;
	}

	h2 {
		margin-top: 0;
		font-size: 1.8rem;
	}

	h3 {
		margin-top: 0;
		font-size: 1.3rem;
	}

	.intro {
		max-width: 650px;
		margin-bottom: 2rem;
		color: var(--muted);
		font-size: 1.2rem;
		line-height: 1.7;
	}

	.buttons {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
	}

	.secondary-button {
		display: inline-block;
		padding: 0.8rem 1.3rem;
		border: 2px solid var(--charcoal);
		border-radius: 0.5rem;
		color: var(--charcoal);
		font-weight: bold;
		text-decoration: none;
	}

	.secondary-button:hover {
		background: var(--charcoal);
		color: white;
	}

	.hero-card {
		padding: 2rem;
		border-top: 5px solid var(--seagrass);
		border-radius: 0.75rem;
		background: var(--surface);
		box-shadow: 0 15px 35px rgba(57, 79, 86, 0.12);
	}

	.hero-card ol {
		margin: 0;
		padding-left: 1.4rem;
		color: var(--muted);
		line-height: 1.8;
	}

	.hero-card li {
		margin-bottom: 0.75rem;
	}

	.about-section {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 4rem;
		align-items: end;
		margin-top: 6rem;
		padding-top: 4rem;
		border-top: 1px solid #d6dada;
	}

	.about-section p:last-child {
		margin-bottom: 0;
		color: var(--muted);
		font-size: 1.1rem;
		line-height: 1.7;
	}

	.cards {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 1.5rem;
		margin-top: 3rem;
	}

	.cards article {
		padding: 2rem;
		border-radius: 0.75rem;
		background: var(--surface);
	}

	.cards article:nth-child(1) {
		border-top: 5px solid var(--seagrass);
	}

	.cards article:nth-child(2) {
		border-top: 5px solid var(--fern);
	}

	.cards article:nth-child(3) {
		border-top: 5px solid var(--wine);
	}

	.cards p {
		margin-bottom: 0;
		color: var(--muted);
		line-height: 1.7;
	}

	.callout {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 2rem;
		margin-top: 5rem;
		padding: 2.5rem;
		border-radius: 0.75rem;
		background: var(--charcoal);
	}

	.callout h2 {
		margin-bottom: 0.5rem;
		color: rgba(255, 255, 255, 0.842);
	}

	.callout p {
		margin: 0;
		color: var(--platinum);
	}

	@media (max-width: 800px) {
		main {
			padding-top: 3rem;
		}

		.hero,
		.about-section,
		.cards {
			grid-template-columns: 1fr;
		}

		.hero {
			gap: 2.5rem;
		}

		.about-section {
			gap: 1rem;
		}

		.callout {
			align-items: flex-start;
			flex-direction: column;
		}
	}
</style>