let posts = JSON.parse(localStorage.getItem('posts')) || [];
    renderPosts();

    function addPost() {
      const text = document.getElementById('textInput').value;
      const imageInput = document.getElementById('imageInput');
      const file = imageInput.files[0];
      
      if (file && text) {
        const reader = new FileReader();
        reader.onloadend = function() {
          const post = { text: text, image: reader.result, comments: [], editing: false };
          posts.unshift(post);
          localStorage.setItem('posts', JSON.stringify(posts));
          renderPosts();
          document.getElementById('textInput').value = '';
          imageInput.value = '';
        };
        reader.readAsDataURL(file);
      }
    }

    function addComment(index) {
      const commentInput = document.getElementById('comment-' + index);
      const comment = commentInput.value;
      if (comment) {
        posts[index].comments.push(comment);
        localStorage.setItem('posts', JSON.stringify(posts));
        renderPosts();
      }
    }

    function editPost(index) {
      posts[index].editing = true;
      renderPosts();
    }

    function savePost(index) {
      const editInput = document.getElementById('edit-' + index);
      posts[index].text = editInput.value;
      posts[index].editing = false;
      localStorage.setItem('posts', JSON.stringify(posts));
      renderPosts();
    }

    function deletePost(index) {
      if (confirm('Tem certeza que deseja excluir este post?')) {
        posts.splice(index, 1);
        localStorage.setItem('posts', JSON.stringify(posts));
        renderPosts();
      }
    }

    function renderPosts() {
      const postsDiv = document.getElementById('posts');
      postsDiv.innerHTML = '';
      posts.forEach((post, index) => {
        const postDiv = document.createElement('div');
        postDiv.className = 'post';
        postDiv.innerHTML = `
          <img src="${post.image}" alt="Post">
          ${post.editing ? 
            `<input type='text' id='edit-${index}' value='${post.text}'><button onclick='savePost(${index})'>Salvar</button>` : 
            `<p>${post.text}</p><button onclick='editPost(${index})'>Editar</button>`}
          <button onclick='deletePost(${index})'>Excluir</button>
          <input type="text" id="comment-${index}" placeholder="Comente aqui..."><br>
          <button onclick="addComment(${index})">Comentar</button>
          <div>
            ${post.comments.map(c => `<div class='comment'>${c}</div>`).join('')}
          </div>
        `;
        postsDiv.appendChild(postDiv);
      });
    }