<template>
    <div class="jumbotron vertical-center">
        <div class="container">
            <!-- Bootswatch -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/sketchy/bootstrap.min.css"
                integrity="sha384-RxqHG2ilm4r6aFRpGmBbGTjsqwfqHOKy1ArsMhHusnRO47jcGqpIQqlQK/kmGy9R" crossorigin="anonymous">
            <div class="row">
                <div class="col-sm-12">
                    <h1 class="text-center bg-primary text-white">Library</h1>
                    <hr><br>
                    <!-- Alert Message -->
                    <b-alert variant="success" v-if="showMessage" show>{{ message }}</b-alert>
                    <!-- Add Product -->
                    <b-button variant="success" v-b-modal.book-modal>Add Product</b-button>
                    <hr><br>
                    <!-- books pagination -->
                    <b-pagination v-model="currentPage" :total-rows="rows" :per-page="perPage" aria-controls="books_table">
                    </b-pagination>
                    <!-- books table -->
                    <b-table id="books_table" :items="books" :per-page="perPage" :current-page="currentPage"
                        :fields="fields">
                        <template #cell(actions)="row">
                            <b-button variant="success" v-b-modal.book-edit-modal
                                @click="editBook(row.item)">Update</b-button>
                            <b-button type="button" class="btn btn-danger btn-sm"
                                @click="deleteBook(row.item)">Delete</b-button>
                        </template>
                    </b-table>
                    <!-- books pagination -->
                    <p>showing {{ item_start }} to {{ item_end }}</p>
                    <b-pagination v-model="currentPage" :total-rows="rows" :per-page="perPage" aria-controls="books_table">
                    </b-pagination>
                    <footer class="bg-primary text-white text-center">Copyright &copy;. All Rights Reserved.</footer>
                </div>
            </div>
            <!-- Add Book Modal -->
            <b-modal ref="addBookModal" id="book-modal" title="Add a new book" hide-backdrop hide-footer>
                <b-form @submit="onSubmit" @reset="onReset" class="w-100">
                    <!-- id -->
                    <b-form-group id="form-id-group" label="id:" label-for="form-id-input">
                        <b-form-input id="form-id-group" type="text" v-model="addBookForm.id" require
                            placeholder="Enter id"></b-form-input>
                    </b-form-group>
                    <!-- Title -->
                    <b-form-group id="form-title-group" label="Title:" label-for="form-title-input">
                        <b-form-input id="form-title-input" type="text" v-model="addBookForm.title" require
                            placeholder="Enter book"></b-form-input>
                    </b-form-group>
                    <!-- Genre -->
                    <b-form-group id="form-genre-group" label="Genre:" label-for="form-genre-input">
                        <b-form-input id="form-genre-input" type="text" v-model="addBookForm.genre" require
                            placeholder="Enter genre"></b-form-input>
                    </b-form-group>
                    <!-- is_read -->
                    <b-form-group id="form-is_read-group">
                        <b-form-checkbox-group v-model="addBookForm.is_read" id="form-checks">
                            <b-form-checkbox value="true">is_read?</b-form-checkbox>
                        </b-form-checkbox-group>
                    </b-form-group>
                    <!-- Submit -->
                    <b-button type="submit" variant="outline-info">Submit</b-button>
                    <!-- reset -->
                    <b-button type="reset" variant="outline-danger">Reset</b-button>
                </b-form>
            </b-modal>
            <!-- Update and Delete Book Modal -->
            <b-modal ref="editBookModal" id="book-edit-modal" title="Update" hide-backdrop hide-footer>
                <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
                    <!-- Title -->
                    <b-form-group id="form-title-edit-group" label="Title:" label-for="form-title-edit-input">
                        <b-form-input id="form-title-input" type="text" v-model="editForm.title" require
                            placeholder="Enter title"></b-form-input>
                    </b-form-group>
                    <!-- Genre -->
                    <b-form-group id="form-genre-edit-group" label="Genre:" label-for="form-genre-edit-input">
                        <b-form-input id="form-genre-edit-input" type="text" v-model="editForm.genre" require
                            placeholder="Enter genre"></b-form-input>
                    </b-form-group>
                    <!-- is_read -->
                    <b-form-group id="form-is_read-edit-group">
                        <b-form-checkbox-group v-model="editForm.is_read" id="form-checks">
                            <b-form-checkbox value="true">is_read?</b-form-checkbox>
                        </b-form-checkbox-group>
                    </b-form-group>
                    <!-- Submit -->
                    <b-button type="submit" variant="outline-info">Update</b-button>
                    <b-button type="reset" variant="outline-danger">Cancel</b-button>
                </b-form>
            </b-modal>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            books: [],
            // add
            addBookForm: {
                id: '',
                title: '',
                genre: '',
                is_read: [],
                date_created: '',
                last_updated: '',
                actions: ''
            },
            // edit
            editForm: {
                id: '',
                title: '',
                genre: '',
                is_read: [],
                date_created: '',
                last_updated: '',
                actions: ''
            },
            // alert
            message: '',
            showMessage: false,
            // Pagination
            perPage: 5,
            currentPage: 1,
            books: [],
            fields: ['id', 'title', 'genre', 'is_read', 'date_created', 'last_updated', 'actions']
        }
    },
    computed: {
        rows() {
            return this.books.length
        },
        item_start() {
            return (this.currentPage - 1) * this.perPage
        },
        item_end() {
            return this.currentPage * this.perPage
        }
    },
    methods: {
        // Get
        getBooks() {
            const path = 'http://127.0.0.1:5000/library'
            axios.get(path)
                .then(res => {
                    this.books = res.data.books
                })
                .catch(err => {
                    console.error(err)
                })
        },
        // Post
        addBook(payLoad) {
            const path = 'http://127.0.0.1:5000/library'
            axios.post(path, payLoad)
                .then(res => {
                    this.getBooks()
                    this.message = 'Book Added!'
                    this.showMessage = true
                })
                .catch(err => {
                    console.error(err);
                    this.getBooks()
                })
        },
        // init
        initForm() {
            // add
            this.addBookForm.id = ''
            this.addBookForm.title = ''
            this.addBookForm.genre = ''
            this.addBookForm.is_read = []
            this.addBookForm.date_created = ''
            this.addBookForm.last_updated = ''
            this.addBookForm.actions = ''
            // edit
            this.editForm.id = ''
            this.editForm.title = ''
            this.editForm.genre = ''
            this.editForm.is_read = []
            this.editForm.date_created = ''
            this.editForm.last_updated = ''
            this.editForm.actions = ''
        },
        onSubmit(e) {
            e.preventDefault()
            this.$refs.addBookModal.hide()
            let is_read = false
            if (this.addBookForm.is_read[0]) {
                is_read = true
            }
            const payLoad = {
                id: this.addBookForm.id,
                title: this.addBookForm.title,
                genre: this.addBookForm.genre,
                is_read,
                date_created: '',
                last_updated: '',
                actions: this.addBookForm.actions
            }
            this.addBook(payLoad)
            this.initForm()
        },
        onReset(e) {
            e.preventDefault()
            this.$refs.addBookModal.hide()
            this.initForm()
        },
        updateBook(payload, bookID) {
            const path = `http://127.0.0.1:5000/library/${bookID}`
            axios.put(path, payload)
                .then(res => {
                    this.getBooks()
                    this.message = 'Book Updated !'
                    this.showMessage = true
                })
                .catch(err => {
                    console.error(err);
                    this.getBooks()
                })
        },
        editBook(book) {
            this.editForm = book
        },
        removeBook(bookID) {
            const path = `http://127.0.0.1:5000/library/${bookID}`
            axios.delete(path)
                .then(res => {
                    this.getBooks()
                    this.message = 'Book Removed !'
                    this.showMessage = true
                })
                .catch(err => {
                    console.error(err);
                    this.getBooks()
                })
        },
        deleteBook(book) {
            this.removeBook(book.id)
        },
        onSubmitUpdate(e) {
            e.preventDefault()
            this.$refs.editBookModal.hide()
            let is_read = false
            if (this.editForm.is_read[0]) {
                is_read = true
            }
            const payload = {
                id: this.editForm.id,
                title: this.editForm.title,
                genre: this.editForm.genre,
                is_read,
                date_created: this.editForm.date_created,
                last_updated: '',
                actions: this.editForm.actions
            }
            this.updateBook(payload, this.editForm.id)
        },
        onResetUpdate(e) {
            e.preventDefault()
            this.$refs.editBookModal.hide()
            this.initForm()
            this.getBooks()
        }
    },
    created() {
        this.getBooks()
    }
}
</script>