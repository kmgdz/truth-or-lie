import https from 'https';
https.get('https://api.github.com/repos/kmgdz/truth-or-lie/commits', { headers: { 'User-Agent': 'node.js' } }, (res) => {
  let data = '';
  res.on('data', d => data += d);
  res.on('end', () => console.log(JSON.parse(data).slice(0, 3).map(c => ({sha: c.sha, message: c.commit.message}))));
});
