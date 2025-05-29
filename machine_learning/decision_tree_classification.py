import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt


def run_social_network_ads():
    df = pd.read_csv("social_network_ads.csv")

    X = df[["Age", "EstimatedSalary"]]
    y = df["Purchased"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)

    clf = DecisionTreeClassifier(max_depth=3, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print("\nSocial Network Ads Dataset")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    plt.figure(figsize=(10, 6))
    plot_tree(clf, feature_names=["Age", "EstimatedSalary"], class_names=[
              "Not Purchased", "Purchased"], filled=True)
    plt.title("Decision Tree - Social Network Ads")
    plt.show()


def run_adult_income():
    df = pd.read_csv("adult_income.csv")

    # Drop ID and preprocess
    df = df.drop(columns=["ID"])
    # One-hot encode categorical variables
    df = pd.get_dummies(df, drop_first=True)

    X = df.drop(columns=["income_high_Yes"])
    y = df["income_high_Yes"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)

    clf = DecisionTreeClassifier(max_depth=5, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print("\nAdult Income Dataset")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    plt.figure(figsize=(16, 8))
    plot_tree(clf, feature_names=X.columns, class_names=[
              "Low", "High"], filled=True, max_depth=3)
    plt.title("Decision Tree - Adult Income (partial view)")
    plt.show()


if __name__ == "__main__":
    run_social_network_ads()
    run_adult_income()
