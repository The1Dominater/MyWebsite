console.log("Loaded JS")

// Allows for static website to use index.html as a template
function loadPage(page) {
  fetch(page)
    .then(response => {
      if (!response.ok) throw new Error("Page not found");
      return response.text();
    })
    .then(html => {
      document.getElementById("content").innerHTML = html;
      // Save the current page choice
      localStorage.setItem("lastPage", page);
      // If portfolio then grab projects from github
      if (page == "portfolio.html") {
        loadTopRepos(username);
      }
    })
    .catch(err => {
      document.getElementById("content").innerHTML = "<p>Error loading page.</p>";
      console.error(err);
    });
}

// Load the saved page (or fallback to home.html) on startup
window.onload = () => {
  const last = localStorage.getItem("lastPage") || "home.html";
  loadPage(last);
};

// Load a list of the top 5 repos on my github
const username = "The1Dominater";
async function loadTopRepos(username, { sortBy = 'stars' } = {}) {
    console.log("Fetching repos")
    const list = document.getElementById('repo-list');
    const url = `https://api.github.com/users/${encodeURIComponent(username)}/repos?type=owner&per_page=100&sort=updated`;

    try {
        console.log("Querying github...")
        const res = await fetch(url, {
        headers: {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        },
        cache: 'no-store'
        });

        console.log("Checking response...")
        if (!res.ok) {
        const text = await res.text().catch(() => '');
        throw new Error(`GitHub API ${res.status} ${res.statusText} — ${text}`);
        }

        const repos = await res.json();

        // Optional: hide forks
        const own = repos.filter(r => !r.fork);

        // Sort
        const sorted = sortBy === 'stars'
        ? own.sort((a, b) => b.stargazers_count - a.stargazers_count)
        : own.sort((a, b) => new Date(b.pushed_at) - new Date(a.pushed_at));

        const top5 = sorted.slice(0, 5);

        // Render
        list.innerHTML = '';
        if (top5.length === 0) {
          list.innerHTML = '<li>No repositories found.</li>';
          return;
        }

        top5.forEach(r => {
          const li = document.createElement('li');
          li.style.listStyle = 'none';
          li.style.margin = '12px 0';

          li.innerHTML = `
            <a href="${r.html_url}" target="_blank" rel="noopener" style="font-size:1.2rem; font-weight:bold; text-decoration:none; color:#0077cc;">
              ${r.name}
            </a>
            <div style="font-size:0.9rem; color:#555; margin-top:4px;">
              ${r.description ? r.description : 'No description provided.'}
            </div>
            <div style="font-size:0.8rem; color:#777; margin-top:2px;">
              ⭐ ${r.stargazers_count} · updated ${new Date(r.pushed_at).toLocaleDateString()}
            </div>
          `;

          list.appendChild(li);
        });

    } catch (err) {
        console.error('Failed to load repos:', err);
        list.innerHTML = `<li>Failed to load repositories. Open DevTools → Console for details.</li>`;
    }
}

// Send emails from the contact form via emailjs
emailjs.init({
  publicKey: 'IMt6LeyFo_NaPYwUa',
  // Do not allow headless browsers
  blockHeadless: true,
  limitRate: {
    // Set the limit rate for the application
    id: 'app',
    // Allow 1 request per 10s
    throttle: 10000,
  },
});


function contactMe(e) {
  //e.preventDefault();
  
  console.log("Attempting to send email...")
  emailjs.sendForm('mywebsite-contactform', 'template_8ntibaq', e.target.form).then(
    (response) => {
      console.log('SUCCESS!', response.status, response.text);
    },
    (error) => {
      console.log('FAILED...', error);
    },
  );

}

