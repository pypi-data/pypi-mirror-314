# Users

Types:

```python
from stainless_demo.types import User, UserListResponse
```

Methods:

- <code title="post /users">client.users.<a href="./src/stainless_demo/resources/users.py">create</a>(\*\*<a href="src/stainless_demo/types/user_create_params.py">params</a>) -> <a href="./src/stainless_demo/types/user.py">User</a></code>
- <code title="get /users/{userId}">client.users.<a href="./src/stainless_demo/resources/users.py">retrieve</a>(user_id) -> <a href="./src/stainless_demo/types/user.py">User</a></code>
- <code title="put /users/{userId}">client.users.<a href="./src/stainless_demo/resources/users.py">update</a>(user_id, \*\*<a href="src/stainless_demo/types/user_update_params.py">params</a>) -> <a href="./src/stainless_demo/types/user.py">User</a></code>
- <code title="get /users">client.users.<a href="./src/stainless_demo/resources/users.py">list</a>(\*\*<a href="src/stainless_demo/types/user_list_params.py">params</a>) -> <a href="./src/stainless_demo/types/user_list_response.py">UserListResponse</a></code>

# Posts

Types:

```python
from stainless_demo.types import Post, PostListResponse
```

Methods:

- <code title="post /posts">client.posts.<a href="./src/stainless_demo/resources/posts.py">create</a>(\*\*<a href="src/stainless_demo/types/post_create_params.py">params</a>) -> <a href="./src/stainless_demo/types/post.py">Post</a></code>
- <code title="get /posts/{postId}">client.posts.<a href="./src/stainless_demo/resources/posts.py">retrieve</a>(post_id) -> <a href="./src/stainless_demo/types/post.py">Post</a></code>
- <code title="put /posts/{postId}">client.posts.<a href="./src/stainless_demo/resources/posts.py">update</a>(post_id, \*\*<a href="src/stainless_demo/types/post_update_params.py">params</a>) -> <a href="./src/stainless_demo/types/post.py">Post</a></code>
- <code title="get /posts">client.posts.<a href="./src/stainless_demo/resources/posts.py">list</a>(\*\*<a href="src/stainless_demo/types/post_list_params.py">params</a>) -> <a href="./src/stainless_demo/types/post_list_response.py">PostListResponse</a></code>
- <code title="delete /posts/{postId}">client.posts.<a href="./src/stainless_demo/resources/posts.py">delete</a>(post_id) -> None</code>
