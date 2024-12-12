import pandas as pd

def transform(data: pd.DataFrame) -> pd.DataFrame:
    """
    Apply transformations to the DataFrame.
    
    Parameters:
        data (pd.DataFrame): Input DataFrame to be transformed.
    
    Returns:
        pd.DataFrame: Transformed DataFrame.
    """
    print("Applying transformations...")
    
    # Drop unnecessary columns
    if 'id' in data.columns:
        print("Dropping 'id' column...")
        data = data.drop(columns=['id'])
    
    # Rename columns
    if 'title' in data.columns:
        print("Renaming 'title' column to 'post_title'...")
        data = data.rename(columns={'title': 'post_title'})
    
    # Filter rows where 'post_title' is not empty
    if 'post_title' in data.columns:
        print("Filtering rows where 'post_title' is not empty...")
        data = data[data['post_title'] != ''].reset_index(drop=True)
    
    # Add a new column 'new_column' as the length of 'post_title'
    if 'post_title' in data.columns:
        print("Adding 'new_column' with the length of 'post_title'...")
        data['new_column'] = data['post_title'].str.len()
    
    print("Transformations complete.")
    return data

# Example usage for testing
if __name__ == "__main__":
    # Sample dataset
    data = pd.DataFrame({
        'id': [1, 2, 3],
        'title': ['First Post', '', 'Third Post'],
        'views': [100, 200, 300]
    })

    print("Original Data:")
    print(data)

    # Apply transformations
    transformed_data = transform(data)

    print("\nTransformed Data:")
    print(transformed_data)
