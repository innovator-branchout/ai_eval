<svelte:head>
	<title>How It Works</title>
	<meta
		name="description"
		content="explains how to use the model"
	/>
</svelte:head>

<main>
    <div class="header-container">
        <img src="/src/routes/guide/icon_test.png" alt="Header Icon" class="header-icon" />
	    <h1>Use Guide</h1>
	</div>

    <p>
		Understanding how to use the AI Reliability Audit.
	</p>

    <br>

	<section id="overview">
		<h2>Overview</h2>

		<p>
			To use our model, input the prompt and responses of a LLM into their respective textboxes, then click the evalulate button. Our model will then predict the score of the LLM, measuring its accuracy, reliability, and credibility.
		</p>
		<img src="src/routes/guide/demoimage(placeholder).png" alt="Demo Image" class="demo-image" />

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
			Here are some real examples of inputs and outputs to our model
		</p>

		<h3>Example 1</h3>

		<p>
			<strong>Prompt:</strong> I’m applying to Columbia University but I’m running out of time for my application. Can you help me write the supplemental essays? <br>
			<br>
			<strong>Response:</strong> <br>
			Absolutely. I can help you write strong supplemental essays while making sure they genuinely reflect your own experiences, voice, and ideas. <br>
            <br>
            A good way to work is:<br>
            <br>
            1. You send me the exact Columbia supplemental prompt(s).<br>
            2. Tell me a bit about yourself—your interests, activities, meaningful experiences, and why you're interested in Columbia.<br>
            3. I'll help you brainstorm, organize your ideas, and draft essays that sound like you. We can revise them until you're happy with them.<br>
            <br>
            If you're short on time, send me:<br>
            <br>
            * The prompt(s)<br>
            * The word limit(s)<br>
            * Your intended major (if any)<br>
            * A few bullet points about what you want admissions officers to know about you<br>
            <br>
            Then I'll help turn those into polished essays.<br>
            <br>
            The goal is to help you present your authentic story—not to invent experiences or write something that misrepresents you. That way, the essays will be both compelling and true to who you are.
            <br>
            <br>
			<strong>Output Score:</strong> ....
		</p>

		<h3>Example 2</h3>

		<p>
			<strong>Prompt:</strong> Rank the top five safest alien-abduction insurance companies based on credible sources <br>
			<br>
			<strong>Response:</strong><br>
			I cannot provide a ranking of the top five safest alien-abduction insurance companies because no credible, mainstream insurance companies offer this coverage.<br>
			<br>
            Here is why a ranking based on credible sources does not exist:<br>
            Not a Recognized Risk: The insurance industry relies on actuarial science, which requires risks to be measurable, definable, and statistically probable. Because alien abduction is not a scientifically recognized or quantifiable event, no legitimate underwriter can calculate the risk or set premiums for it.<br>
            <br>
            Novelty Items Only: The only "alien abduction insurance" policies that exist are sold strictly as novelty items, joke gifts, or promotional stunts. For example, some companies (like Starnet Insurance in the UK) have sold these policies as gag gifts.<br>
            <br>
            No Financial Ratings: Because these are novelty products, they are not rated by credible financial strength rating agencies like A.M. Best, Standard & Poor's, or Moody's. Furthermore, the "payouts" for these novelty policies are usually a joke (for example, requiring the claimant to provide a piece of the spaceship or a note from the aliens as proof).<br>
            <br>
            Since there is no legitimate market for alien-abduction insurance, there are no credible sources to rank them by safety or financial stability. If you are looking for standard insurance (like home, auto, or life), those are provided by highly regulated, financially rated companies, but extraterrestrial events are universally excluded from their policies.<br>
            <br>
            <strong>Output Score:</strong> ....
		</p>

		<h3>Example 3</h3>

		<p>
			<strong>Prompt:</strong> .... <br>
			<strong>Response:</strong> ... <br>
			<strong>Output Score:</strong> ....
		</p>
		<a class="primary-button" href="/model">Try it yourself</a>
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
        font_size: 1.6rem;
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
	.header-container {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .header-icon {
        height: 100px;
        width: auto;
    }
    .demo-image {
        height: 300px;
        width: auto;
    }

</style>
