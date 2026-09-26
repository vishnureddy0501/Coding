morris inorder traversal:
-----------------------------

void morrisTraversal(TreeNode* root) {
    TreeNode* curr = root;
    
    while (curr != nullptr) {
        if (curr->left == nullptr) {
            std::cout << curr->val << " ";
            curr = curr->right;
        } else {
            // Find the inorder predecessor of curr
            TreeNode* pre = curr->left;
            while (pre->right != nullptr && pre->right != curr) {
                pre = pre->right;
            }

            if (pre->right == nullptr) {
                // Make curr the right child of its inorder predecessor
                pre->right = curr;
                curr = curr->left;
            } else {
                // Revert the changes made (thread removal)
                pre->right = nullptr;
                std::cout << curr->val << " ";
                curr = curr->right;
            }
        }
    }
}

morris preorder traversal:
--------------------------
void morrisTraversal(TreeNode* root) {
    TreeNode* curr = root;
    
    while (curr != nullptr) {
        if (curr->left == nullptr) {
            std::cout << curr->val << " ";
            curr = curr->right;
        } else {
            TreeNode* pre = curr->left;
            while (pre->right != nullptr && pre->right != curr) {
                pre = pre->right;
            }

            if (pre->right == nullptr) {
                pre->right = curr;
				std::cout << curr->val << " ";
                curr = curr->left;
            } else {
                pre->right = nullptr;
                curr = curr->right;
            }
        }
    }
}

