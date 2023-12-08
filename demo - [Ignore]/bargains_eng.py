import json
from difflib import SequenceMatcher

def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {file_path}")
        return []

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_product(data, product_name):
    product_name_lower = product_name.lower()
    for product in data:
        if product_name_lower in product['title'].lower():
            return product
    return None

def recommend_products(data, base_product, other_database):
    base_text = base_product['title'] + ' ' + ' '.join(base_product.get('details', []))
    recommendations = []
    other_db_recommendation_added = False

    # First, find recommendations in the same database
    for product in data:
        if product == base_product:
            continue
        product_text = product['title'] + ' ' + ' '.join(product.get('details', []))
        sim_score = similarity(base_text, product_text)
        if sim_score >= 0.5:
            recommendations.append((product, sim_score))

    # Then, ensure at least one recommendation from the other database
    for product in other_database:
        if product == base_product:
            continue
        product_text = product['title'] + ' ' + ' '.join(product.get('details', []))
        sim_score = similarity(base_text, product_text)
        if sim_score >= 0.4:
            recommendations.append((product, sim_score))
            other_db_recommendation_added = True
            break

    # If no recommendation from the other database, add the most similar one
    if not other_db_recommendation_added:
        max_sim_score = 0
        most_similar_product = None
        for product in other_database:
            if product == base_product:
                continue
            product_text = product['title'] + ' ' + ' '.join(product.get('details', []))
            sim_score = similarity(base_text, product_text)
            if sim_score > max_sim_score:
                max_sim_score = sim_score
                most_similar_product = product
        if most_similar_product:
            recommendations.append((most_similar_product, max_sim_score))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations


class Bargains:
    def __init__(self, database1_path, database2_path):
        self.database1 = load_data(database1_path)
        self.database2 = load_data(database2_path)

    def search(self, product_name):
        product = find_product(self.database1, product_name)
        database_used = self.database1
        other_database = self.database2

        if not product:
            product = find_product(self.database2, product_name)
            database_used = self.database2
            other_database = self.database1

        if not product:
            return "Product not found."

        recommendations = recommend_products(database_used, product, other_database)

        # Formatting the output
        output = f"Product Found:\nTitle: {product['title']}\nPrice: {product.get('price', 'N/A')}\nURL: {product.get('url', 'N/A')}\nPhoto: {product.get('photo', 'N/A')}\n"
        if 'details' in product:
            output += "Details:\n" + "\n".join(product['details']) + "\n"

        output += "\nRecommendations:\n"
        for rec_product, sim_score in recommendations:
            output += f"Title: {rec_product['title']}\nSimilarity: {sim_score:.2f}\nPrice: {rec_product.get('price', 'N/A')}\nURL: {rec_product.get('url', 'N/A')}\n\n"

        return output




# Example usage
# bargains_module = Bargains(['path_to_json1.json', 'path_to_json2.json'])
# print(bargains_module.search('Tecno pop 8'))

database1_path = "demo/db/db-A.json"
database2_path = "demo/db/db-B.json"
bargains_module = Bargains(database1_path, database2_path )
print(bargains_module.search('Tecno POP'))


## Limitation ##

## There's no user profile to perform collaborative filtering with
# The dataset size is too small for the algorithm
# Real time price comparison needs microserves that with scheduled runs.abs