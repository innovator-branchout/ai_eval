<svelte:head>
	<title>AI Reliability Audit</title>
	<meta
		name="description"
		content="wow"
	/>
</svelte:head>

<main>
	<h1>AI Reliability Audit</h1>

  <nav class="menu-bar">
    <!a href="index.html">Home</a>
    <a href="app.html">About</a>
    <a href="contact.html">Contact</a>
    <a href="https://www.instagram.com/branchoutveritas/">Instagram</a>
  </nav>

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
    .menu-bar {
      background-color: #394f56;
      text-align: center;
      padding: 12px 0;
    }

    .menu-bar a {
      color: white;
      text-decoration: none;
      font-family: Georgia, "Times New Roman", serif;
      font-size: 18px;
      font-weight: bold;
      margin: 0 18px;
    }

    .menu-bar a:hover {
      text-decoration: underline;
    }
    
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

	section {
		margin-top: 6rem;
		padding: 2rem;
		border-left: 5px solid var(--seagrass);
		border-radius: 0.5rem;
		background: var(--surface);
	}
</style>