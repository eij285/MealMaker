import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom';
import { ThemeProvider } from '@emotion/react';
import { GlobalProvider } from './utils/GlobalContext';
import theme from './theme.js';
import AuthorisedRoute from './utils/AuthorisedRoute';
import HomePage from './pages/HomePage';
import LoginPage from './pages/Auth/LoginPage';
import SignupPage from './pages/Auth/SignupPage';
import ForgotPasswordPage from './pages/Auth/ForgotPasswordPage';
import PasswordResetPage from './pages/Auth/PasswordResetPage';
import DashboardPage from './pages/DashboardPage';
import UserProfilePage from './pages/User/UserProfilePage';
import UpdatePasswordPage from './pages/Auth/UpdatePasswordPage';
import UserPreferencesPage from './pages/User/UserPreferencesPage';
import UserPublicPage from './pages/User/UserPublicPage';
import MyRecipesPage from './pages/Recipe/MyRecipesPage';
import CreateRecipePage from './pages/Recipe/CreateRecipePage';
import EditRecipePage from './pages/Recipe/EditRecipePage';
import ViewRecipePage from './pages/Recipe/ViewRecipePage';
import SearchPage from './pages/SearchPage';
import FollowingPage from './pages/User/FollowingPage';
import FollowersPage from './pages/User/FollowersPage';
import MyCookbooksPage from './pages/Cookbook/MyCookbooksPage';
import CreateCookbookPage from './pages/Cookbook/CreateCookbookPage';
import EditCookbookPage from './pages/Cookbook/EditCookbookPage';
import ViewCookbookPage from './pages/Cookbook/ViewCookbookPage';
import MessageRoomsPage from './pages/Message/MessageRoomsPage';
import SingleMessageRoomPage from './pages/Message/SingleMessageRoomPage';
import ManageShoppingPage from './pages/Shopping/ManageShoppingPage';
import AddEditPaymentMethodPage from './pages/Shopping/AddEditPaymentMethodPage';
import ShoppingCartPage from './pages/Shopping/ShoppingCartPage';
import CheckoutPage from './pages/Shopping/CheckoutPage';
import ViewCartPage from './pages/Shopping/ViewCartPage';
import Forbidden403Page from './pages/Error/Forbidden403Page';
import NotFound404Page from './pages/Error/NotFound404Page';
import './App.css';

function App() {
  return (
    <GlobalProvider>
      <ThemeProvider theme={theme}>
        <Router>
          <Routes>
            <Route exact path="/" element={<HomePage />} />
            <Route exact path="/login" element={<LoginPage />} />
            <Route exact path="/signup" element={<SignupPage />} />
            <Route exact path="/forgot-password" element={<ForgotPasswordPage />} />
            <Route exact path="/password-reset" element={<PasswordResetPage />} />
            <Route path="/user/:userId" element={<UserPublicPage />} />
            <Route path="/recipe/:recipeId" element={<ViewRecipePage />} />
            <Route path="/cookbook/:cookbookId" element={<ViewCookbookPage />} />
            <Route path="/search" order={0} element={<SearchPage />} />
            <Route path="/search/:query" order={1} element={<SearchPage />} />
            <Route element={<AuthorisedRoute />}>
              <Route exact path="/dashboard" element={<DashboardPage />} />
              <Route exact path="/user-profile" element={<UserProfilePage />} />
              <Route exact path="/update-password" element={<UpdatePasswordPage />} />
              <Route exact path="/user-preferences" element={<UserPreferencesPage />} />
              <Route exact path="/my-recipes" element={<MyRecipesPage />} />
              <Route exact path="/create-recipe" element={<CreateRecipePage />} />
              <Route path="/edit-recipe/:recipeId" element={<EditRecipePage />} />
              <Route exact path="/following" element={<FollowingPage />} />
              <Route exact path="/followers" element={<FollowersPage />} />
              <Route exact path="/my-cookbooks" element={<MyCookbooksPage/>} />
              <Route exact path="/create-cookbook" element={<CreateCookbookPage />} />
              <Route path="/edit-cookbook/:cookbookId" element={<EditCookbookPage />} />
              <Route exact path="/message-rooms" element={<MessageRoomsPage /> } />
              <Route path="/message-room/:roomId" element={<SingleMessageRoomPage />} />
              <Route exact path="/manage-shopping" element={<ManageShoppingPage />} />
              <Route exact path="/add-payment-method" element={<AddEditPaymentMethodPage />} />
              <Route path="/edit-payment-method/:methodId" element={<AddEditPaymentMethodPage />} />
              <Route exact path="/cart" element={<ShoppingCartPage />} />
              <Route exact path="/checkout" element={<CheckoutPage />} />
              <Route exact path="/view-cart/:cartId" element={<ViewCartPage />} />
            </Route>
            <Route exact path="/forbidden-403" element={<Forbidden403Page />} />
            <Route path="*" element={<NotFound404Page />} />
          </Routes>
        </Router>
      </ThemeProvider>
    </GlobalProvider>
  );
}

export default App;
