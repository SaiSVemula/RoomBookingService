<!-- LoginSignup.vue -->
<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <h2>Login</h2>
                <form @submit.prevent="handleLogin">
                    <div class="mb-3">
                        <label for="loginEmail" class="form-label">Email</label>
                        <input type="email" class="form-control" id="loginEmail" v-model="loginEmail" required>
                    </div>
                    <div class="mb-3">
                        <label for="loginPassword" class="form-label">Password</label>
                        <input type="password" class="form-control" id="loginPassword" v-model="loginPassword" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Login</button>
                </form>

                <div v-if="showSignup" class="mt-5">
                    <h2>Signup</h2>
                    <form @submit.prevent="handleSignup">
                        <div class="mb-3">
                            <label for="signupEmail" class="form-label">Email</label>
                            <input type="email" class="form-control" id="signupEmail" v-model="signupEmail" required>
                        </div>
                        <div class="mb-3">
                            <label for="signupPassword" class="form-label">Password</label>
                            <input type="password" class="form-control" id="signupPassword" v-model="signupPassword"
                                required>
                        </div>
                        <div class="mb-3">
                            <label for="signupPasswordConfirm" class="form-label">Re-enter Password</label>
                            <input type="password" class="form-control" id="signupPasswordConfirm"
                                v-model="signupPasswordConfirm" required>
                        </div>
                        <div class="mb-3">
                            <label for="staffType" class="form-label">Staff Type</label>
                            <select class="form-select" id="staffType" v-model="staffType" required>
                                <option value="">Select Staff Type</option>
                                <option value="Admin">Admin</option>
                                <option value="Professors">Professors</option>
                                <option value="Student">Student</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="firstName" class="form-label">First Name</label>
                            <input type="text" class="form-control" id="firstName" v-model="firstName" required>
                        </div>
                        <div class="mb-3">
                            <label for="lastName" class="form-label">Last Name</label>
                            <input type="text" class="form-control" id="lastName" v-model="lastName" required>
                        </div>
                        <div class="mb-3">
                            <label for="school" class="form-label">School</label>
                            <select class="form-select" id="school" v-model="school" required>
                                <option value="">Select School</option>
                                <option value="School of the Arts">School of the Arts</option>
                                <option value="School of Business and Management">School of Business and Management</option>
                                <option value="School of Economics and Finance">School of Economics and Finance</option>
                                <option value="School of Geography">School of Geography</option>
                                <option value="School of History">School of History</option>
                                <option value="School of Law">School of Law</option>
                                <option value="School of politics and International Relations">School of politics and International Relations</option>
                                <option value="School of Medicine and Dentistry">School of Medicine and Dentistry</option>
                                <option value="School of Biological and Behavioural Sciences">School of Biological and Behavioural Sciences</option>
                                <option value="School of Electronic Engineering and Computer Science">School of Electronic Engineering and Computer Science</option>
                                <option value="School of Engineering and Materials Science">School of Engineering and Materials Science</option>
                                <option value="School of Mathematical Sciences">School of Mathematical Sciences</option>
                                <option value="School of physical and Chemical Sciences">School of physical and Chemical Sciences</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-success">Signup</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            loginEmail: '',
            loginPassword: '',
            signupEmail: '',
            signupPassword: '',
            signupPasswordConfirm: '',
            staffType: '',
            firstName: '',
            lastName: '',
            school: '',
            showSignup: false,
        };
    },
    methods: {
        async handleLogin() {
            // Replace this with your actual user verification logic
            const userExists = await this.checkUserExists(this.loginEmail, this.loginPassword);
            if (userExists) {
                // Store user email and ID in cookies
                this.setCookie('userEmail', this.loginEmail, 1);
                this.setCookie('userId', userExists.id, 1);
                // Redirect to app.vue
                this.$router.push('/app');
            } else {
                // Show signup form with email pre-filled
                this.signupEmail = this.loginEmail;
                this.showSignup = true;
            }
        },
        async handleSignup() {
            if (this.signupPassword !== this.signupPasswordConfirm) {
                alert('Passwords do not match.');
                return;
            }
            // Replace this with your actual signup logic
            const newUser = {
                email: this.signupEmail,
                password: this.signupPassword,
                staffType: this.staffType,
                firstName: this.firstName,
                lastName: this.lastName,
                school: this.school,
            };
            await this.createUser(newUser);
            // Store user email and ID in cookies
            this.setCookie('userEmail', this.signupEmail, 1);
            this.setCookie('userId', newUser.id, 1);
            // Redirect to app.vue
            this.$router.push('/app');
        },
        async checkUserExists(email, password) {
            // This method should call your backend to verify user credentials
            // For now, you can mock it
            return null; // Return user object if exists, null otherwise
        },
        async createUser(user) {
            // This method should call your backend to create a new user
        },
        setCookie(name, value, days) {
            const d = new Date();
            d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
            const expires = "expires=" + d.toUTCString();
            document.cookie = name + "=" + value + ";" + expires + ";path=/";
        },
    },
};
</script>