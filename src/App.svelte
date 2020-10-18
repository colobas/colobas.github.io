<script>
  import router from 'page'

  import Home from './routes/Home.svelte'
  import Post from './routes/Post.svelte'
  
  let page
  let params
  

  router('/', () => (page = Home))
  router(
    '/post/:type/:id',

    (ctx, next) => {
      params = ctx.params
      next()
    },

    () => (page = Post)
  )

  router.start()
</script>


<svelte:component this="{page}" params="{params}" />
