# ProfilePortfolioContent.tsx

## Description
The `ProfilePortfolioContent.tsx` file is a React component that displays a user's portfolio. It takes in an array of portfolio items as a prop and renders each item with its title, description, and URL. The component also provides functionality to add new portfolio items, change the position of existing items, and remove items from the portfolio.

## Examples
Here are a few examples of how to use the `ProfilePortfolioContent` component:

```jsx
import { ProfilePortfolioContent } from './ProfilePortfolioContent';

const portfolio = [
  {
    title: 'Project 1',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    url: 'https://example.com/project1',
  },
  {
    title: 'Project 2',
    description: 'Nulla facilisi. Sed euismod nunc auctor, aliquet libero vitae.',
    url: 'https://example.com/project2',
  },
];

const App = () => {
  return (
    <div>
      <h1>My Portfolio</h1>
      <ProfilePortfolioContent
        portfolio={portfolio}
        onWantToChangeIndex={(index) => console.log(`Change position of item ${index}`)}
        onClickAddNew={() => console.log('Add new portfolio item')}
        onClickRemove={(index) => console.log(`Remove item ${index}`)}
      />
    </div>
  );
};

export default App;
```

## Methods

### ProfilePortfolioContent
The `ProfilePortfolioContent` component is the main component that renders the portfolio items.

#### Props
- `portfolio` (Array): An array of portfolio items.
- `onWantToChangeIndex` (Function): A callback function that is called when the user wants to change the position of a portfolio item. It takes the index of the item as a parameter.
- `onClickAddNew` (Function): A callback function that is called when the user clicks the "Add new" button to add a new portfolio item.
- `onClickRemove` (Function): A callback function that is called when the user clicks the trash icon to remove a portfolio item. It takes the index of the item as a parameter.

### TrashIcon
The `TrashIcon` component is a reusable SVG icon component that represents a trash can.

## Technical Concepts
- React Hooks: The `useState` hook from the `react` library is used in this file to manage the state of the `openedItem` variable. It allows the component to keep track of the currently opened portfolio item.

## Template Variables
There are no template variables used in this file.

## Template File
This file does not contain a template.