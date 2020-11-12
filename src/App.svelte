<script>
  import Router from 'svelte-spa-router'

  import Home from './routes/Home.svelte'
  import Post from './routes/Post.svelte'

  const routes = {
    '/': Home,
    '/post/:type/:id': Post,
  }
  
</script>

<body>
  <Router {routes}/>
</body>
