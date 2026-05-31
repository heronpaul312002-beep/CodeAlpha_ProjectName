            gap: 2rem;
        }

        /* Flashcard Container & Flip Animation */
        .flashcard-container {
            perspective: 1000px;
            width: 100%;
            height: 300px;
            cursor: pointer;
        }

        .flashcard {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 1rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        }

        .flashcard.flipped {
            transform: rotateY(180deg);
        }

        .card-face {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 1rem;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: var(--card-bg);
            border: 1px solid var(--border);
        }

        .card-back {
            transform: rotateY(180deg);
            background-color: #f5f3ff;
            border-color: #ddd6fe;
        }

        .card-label {
            position: absolute;
            top: 1rem;
            left: 1rem;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-light);
        }

        .card-content {
            font-size: 1.5rem;
            font-weight: 600;
            word-break: break-word;
        }

        /* Controls */
        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
        }

        button {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 0.5rem;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        .btn-primary {
            background-color: var(--primary);
            color: white;
        }

        .btn-primary:hover {
            background-color: var(--primary-hover);
        }

        .btn-secondary {
            background-color: transparent;
            border: 1px solid var(--border);
            color: var(--text);
        }

        .btn-secondary:hover {
            background-color: #e2e8f0;
        }

        .btn-danger {
            background-color: var(--danger);
            color: white;
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
        }

        .btn-danger:hover {
            background-color: var(--danger-hover);
        }

        .card-counter {
            font-weight: 600;
            color: var(--text-light);
        }

        /* Creator / Manager Section */
        .manager-section {
            background: var(--card-bg);
            border-radius: 1rem;
            padding: 1.5rem;
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }

        .manager-section h2 {
            font-size: 1.25rem;
            margin-bottom: 1rem;
            color: var(--text);
        }

        .form-group {
            margin-bottom: 1rem;
        }

        .form-group label {
            display: block;
            font-size: 0.875rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: var(--text-light);
        }

        .form-group textarea {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            resize: vertical;
            min-height: 80px;
            font-family: inherit;
            font-size: 0.95rem;
        }

        .form-group textarea:focus {
            outline: 2px solid var(--primary);
            border-color: transparent;
        }

        .form-actions {
            display: flex;
            gap: 0.5rem;
        }

        /* Flashcard List */
        .flashcard-list {
            margin-top: 1.5rem;
            border-top: 1px solid var(--border);
            padding-top: 1.5rem;
            max-height: 300px;
            overflow-y: auto;
        }

        .list-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem;
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
            background: var(--bg);
        }

        .list-item-text {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 70%;
            font-size: 0.9rem;
        }

        .list-item-actions {
            display: flex;
            gap: 0.25rem;
        }

        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            background: var(--card-bg);
            border-radius: 1rem;
            border: 2px dashed var(--border);
            color: var(--text-light);
        }
    </style>
</head>
<body>

    <header>
        <h1>Flashcard Quizzer</h1>
        <p>Boost your memory with interactive study sets</p>
    </header>

    <div class="container">
        <div id="quiz-view">
            <div class="flashcard-container" onclick="toggleFlip()">
                <div class="flashcard" id="flashcard">
                    <div class="card-face card-front">
                        <span class="card-label">Question</span>
                        <div class="card-content" id="front-text">What is the capital of France?</div>
                    </div>
                    <div class="card-face card-back">
                        <span class="card-label">Answer</span>
                        <div class="card-content" id="back-text">Paris</div>
                    </div>
                </div>
            </div>

            <div class="controls" style="margin-top: 1.5rem;">
                <button class="btn-secondary" id="prev-btn" onclick="prevCard()">← Prev</button>
                <button class="btn-primary" id="flip-btn" onclick="toggleFlip()">Show Answer</button>
                <span class="card-counter" id="card-counter">1 / 1</span>
                <button class="btn-secondary" id="next-btn" onclick="nextCard()">Next →</button>
            </div>
        </div>

        <div id="empty-view" class="empty-state" style="display: none;">
            <h3>No Flashcards Available</h3>
            <p>Use the creator below to add your first flashcard!</p>
        </div>

        <div class="manager-section">
            <h2 id="form-title">Create New Flashcard</h2>
            <form id="flashcard-form" onsubmit="handleFormSubmit(event)">
                <input type="hidden" id="edit-id" value="">
                <div class="form-group">
                    <label for="card-question">Question</label>
                    <textarea id="card-question" required placeholder="Enter your question here..."></textarea>
                </div>
                <div class="form-group">
                    <label for="card-answer">Answer</label>
                    <textarea id="card-answer" required placeholder="Enter the answer here..."></textarea>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn-primary" id="save-btn">Add Flashcard</button>
                    <button type="button" class="btn-secondary" id="cancel-btn" onclick="resetForm()" style="display: none;">Cancel</button>
                </div>
            </form>

            <div class="flashcard-list" id="flashcard-list">
                </div>
        </div>
    </div>

    <script>
        // Initial / Default Flashcards
        const defaultCards = [
            { id: 1710000000001, question: "What is the Big O time complexity of searching a binary search tree (balanced)?", answer: "O(log n)" },
            { id: 1710000000002, question: "What does HTML stand for?", answer: "HyperText Markup Language" },
            { id: 1710000000003, question: "Which JavaScript keyword is used to declare a block-scoped variable that can be reassigned?", answer: "let" }
        ];

        // App State
        let flashcards = JSON.parse(localStorage.getItem('flashcards')) || defaultCards;
        let currentIndex = 0;
        let isFlipped = false;

        // Elements
        const flashcardEl = document.getElementById('flashcard');
        const frontTextEl = document.getElementById('front-text');
        const backTextEl = document.getElementById('back-text');
        const flipBtn = document.getElementById('flip-btn');
        const counterEl = document.getElementById('card-counter');
        const quizView = document.getElementById('quiz-view');
        const emptyView = document.getElementById('empty-view');
        const listContainer = document.getElementById('flashcard-list');
        
        // Form Elements
        const formTitle = document.getElementById('form-title');
        const questionInput = document.getElementById('card-question');
        const answerInput = document.getElementById('card-answer');
        const editIdInput = document.getElementById('edit-id');
        const saveBtn = document.getElementById('save-btn');
        const cancelBtn = document.getElementById('cancel-btn');

        // Initialize App
        function initApp() {
            updateQuizUI();
            renderManageList();
        }

        // Save to local storage
        function saveToStorage() {
            localStorage.setItem('flashcards', JSON.stringify(flashcards));
        }

        // Update the Quiz Card Display
        function updateQuizUI() {
            if (flashcards.length === 0) {
                quizView.style.display = 'none';
                emptyView.style.display = 'block';
                return;
            }

            quizView.style.display = 'block';
            emptyView.style.display = 'none';

            // Reset rotation state smoothly before content change if moving cards
            if (isFlipped) {
                flashcardEl.classList.remove('flipped');
                isFlipped = false;
                flipBtn.textContent = "Show Answer";
            }

            // Bind data
            const currentCard = flashcards[currentIndex];
            frontTextEl.textContent = currentCard.question;
            backTextEl.textContent = currentCard.answer;

            // Counter update
            counterEl.textContent = `${currentIndex + 1} / ${flashcards.length}`;
        }

        // Flip functionality
        function toggleFlip() {
            if (flashcards.length === 0) return;
            isFlipped = !isFlipped;
            if (isFlipped) {
                flashcardEl.classList.add('flipped');
                flipBtn.textContent = "Show Question";
            } else {
                flashcardEl.classList.remove('flipped');
                flipBtn.textContent = "Show Answer";
            }
        }

        // Navigation
        function nextCard() {
            if (flashcards.length === 0) return;
            currentIndex = (currentIndex + 1) % flashcards.length;
            updateQuizUI();
        }

        function prevCard() {
            if (flashcards.length === 0) return;
            currentIndex = (currentIndex - 1 + flashcards.length) % flashcards.length;
            updateQuizUI();
        }

        // Render CRUD Manager List
        function renderManageList() {
            listContainer.innerHTML = '';
            
            flashcards.forEach((card) => {
                const item = document.createElement('div');
                item.className = 'list-item';
                item.innerHTML = `
                    <div class="list-item-text"><strong>Q:</strong> ${card.question}</div>
                    <div class="list-item-actions">
                        <button class="btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.8rem;" onclick="startEdit(${card.id})">Edit</button>
                        <button class="btn-danger" onclick="deleteCard(${card.id})">Delete</button>
                    </div>
                `;
                listContainer.appendChild(item);
            });
        }

        // Handle Add or Edit Submission
        function handleFormSubmit(e) {
            e.preventDefault();
            const question = questionInput.value.trim();
            const answer = answerInput.value.trim();
            const editId = editIdInput.value;

            if (!question || !answer) return;

            if (editId) {
                // Edit existing card
                flashcards = flashcards.map(card => 
                    card.id === parseInt(editId) ? { ...card, question, answer } : card
                );
                resetForm();
            } else {
                // Create new card
                const newCard = {
                    id: Date.now(),
                    question,
                    answer
                };
                flashcards.push(newCard);
                // Move view to the newly added card
                currentIndex = flashcards.length - 1;
                resetForm();
            }

            saveToStorage();
            updateQuizUI();
            renderManageList();
        }

        // Enter editing mode
        function startEdit(id) {
            const cardToEdit = flashcards.find(card => card.id === id);
            if (!cardToEdit) return;

            formTitle.textContent = "Edit Flashcard";
            questionInput.value = cardToEdit.question;
            answerInput.value = cardToEdit.answer;
            editIdInput.value = cardToEdit.id;
            saveBtn.textContent = "Save Changes";
            cancelBtn.style.display = 'inline-block';
            
            // Scroll to form smoothly
            formTitle.scrollIntoView({ behavior: 'smooth' });
        }

        // Reset form to default "Add" state
        function resetForm() {
            formTitle.textContent = "Create New Flashcard";
            questionInput.value = '';
            answerInput.value = '';
            editIdInput.value = '';
            saveBtn.textContent = "Add Flashcard";
            cancelBtn.style.display = 'none';
        }

        // Delete function
        function deleteCard(id) {
            // Confirm deletion
            if(!confirm("Are you sure you want to delete this flashcard?")) return;

            // Find index of targeted delete card
            const targetIndex = flashcards.findIndex(card => card.id === id);
            
            flashcards.splice(targetIndex, 1);

            // Handle current index bounds adjustments
            if (currentIndex >= flashcards.length && flashcards.length > 0) {
                currentIndex = flashcards.length - 1;
            } else if (flashcards.length === 0) {
                currentIndex = 0;
            }

            // If we deleted a card we were currently editing, reset the form
            if (editIdInput.value === id.toString()) {
                resetForm();
            }

            saveToStorage();
            updateQuizUI();
            renderManageList();
        }

        // Keyboard Shortcuts for accessibility
        document.addEventListener('keydown', (e) => {
            // Avoid triggers when typing inside inputs or textareas
            if (document.activeElement.tagName === 'TEXTAREA' || document.activeElement.tagName === 'INPUT') {
                return;
            }
            
            if (e.code === 'Space') {
                e.preventDefault();
                toggleFlip();
            } else if (e.code === 'ArrowRight') {
                nextCard();
            } else if (e.code === 'ArrowLeft') {
                prevCard();
            }
        });

        // Bootstrap Application
        initApp();
    </script>
</body>
</html>
