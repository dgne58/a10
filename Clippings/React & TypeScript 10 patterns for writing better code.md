---
title: "React & TypeScript: 10 patterns for writing better code"
source: "https://blog.logrocket.com/react-typescript-10-patterns-writing-better-code/"
author:
  - "[[Peter Aideloje]]"
published: 2025-07-10
created: 2026-04-13
description: "This article explores several proven patterns for writing safer, cleaner, and more readable code in React and TypeScript."
tags:
  - "clippings"
---
Building a scalable and maintainable React application is often accompanied by a series of challenges, including a lack of type safety, growing pains as projects expand, unreliable prop validation, and brittle DOM manipulation. While most of these issues can be handled by plain JavaScript, it lacks the guardrails required for long-term confidence in your codebase. That’s where TypeScript comes in to solve these recurring issues in a consistent and scalable way.

![React & TypeScript: 10 Patterns For Writing Better Code](https://blog.logrocket.com/wp-content/uploads/2025/06/react-typescript-10-patterns-writing-better-code.png)

In this article, we’ll explore several proven patterns for writing safer, cleaner, and more readable code in React and TypeScript.

## Benefits of using TypeScript in React

[TypeScript offers several advantages](https://blog.logrocket.com/how-to-use-typescript-react-tutorial-examples/) when used with a React application, including code quality and developer productivity:

- **Maintainability**: It makes code more readable and self-documenting, which helps teams manage and scale projects effectively
- **Early error detection**: It identifies bugs at compile time, allowing developers to resolve issues before they even affect end users
- **Better tooling**: It provides superior IDE support with features like auto-completion, refactoring, and code navigation for a smoother development experience
- **Type safety**: Catches type-related errors during development, reducing runtime bugs and improving code reliability
- **Confidence in refactoring**: It enables safer code changes by ensuring that incorrect type usage is flagged immediately

### Typed component props and default props

In TypeScript, interfaces are useful when describing component props, especially when you need to extend or implement them in multiple places. Here’s how you can declare and use props with an interface:

```typescript
import React from 'react';

   interface MyEmployeeProps {
     name: string;
     age: number;
     isEmployed?: boolean; // Optional property
   }

   const MyEmployee: React.FC<MyEmployeeProps> = ({
         name, 
         age, 
         isEmployed }) => {
     return (
       <div>
         <p>Name: {name}</p>
         <p>Age: {age}</p>
         {isEmployed !== undefined && <p>Employed: {isEmployed ? 'Yes' : 'No'}</p>}
       </div>
     );
   };

   export default MyEmployee;
```

You can also use `type` in place of `interfaces` if you’re composing types with unions or intersections, but for extensibility, `interfaces` are often preferred:

```typescript
import React from 'react';

   type SubmitButtonProps = {
     text: string;
     onClick: () => void;
     variant?: 'primary' | 'secondary'; // Union type
   };

   const UserButton: React.FC<SubmitButtonProps> = ({
           text,
           onClick,
           variant }) => {
     return (
       <button onClick={onClick} className={variant === 'primary' ? 'primary-button' : 'secondary-button'}>
         {text}
       </button>
     );
   };

   export default UserButton;
```

In TypeScript with React, component props are treated as required unless you add a `?` to mark one as optional. That rule holds true whether you use an interface or a type alias to describe the props.

#### required props:

```typescript
interface MyEmployeeProps {
  requiredFullName: string;
  requiredAge: number;
}

const MyEmployee: React.FC<MyEmployeeProps> = ({
     requiredFullName,
     requiredAge}) => {
  return (
    <div>
      {requiredFullName} {requiredAge}
    </div>
  );
};
```

From the above, it is clear that `requiredFullName` and `requiredAge` are both required, and TypeScript will enforce this at compile-time by throwing an error.

#### optional props:

```typescript
interface MyEmployeeProps {
  requiredFullName: string;
  optionalAge?: number;
}
const MyEmployee: React.FC<MyEmployeeProps> = ({ 
      requiredFullName,
      optionalAge }) => {
  return (
    <div>
      {requiredFullName} {optionalAge}
    </div>
  );
};
```

The `optionalAge` is marked with a `?`, which indicates that it’s `optional` and can be safely omitted when using the component without causing any TypeScript errors.

#### default props and default parameter values (functional components):

```typescript
//this is the class component
class UserComponent extends React.Component<UserProps> {
         render(){
          return <div style={{ color: this.props.color, fontSize: this.props.fontSize
          }}>{this.props.title}</div>;
                }
             }

       UserComponent.defaultProps = {
           color: 'blue'
           fontSize: 20,
       };

    //this is the functional component (FC)
    const UserFunctionalComponent: React.FC<UserProps> = ({ 
            title, 
            color = "blue", 
            fontSize = 20 }) => {
               return <div style={{ color: color, fontSize: fontSize }}>{title}</div>;
            };
```

By using the `defaultProps ` property for class components, you’re able to set default values for props to ensure components behave in a predictable way even when some props are not provided. While in the functional components, you only need to assign default values directly in the function parameters for any optional props. This will make your code cleaner and also a guaranteed way to prevent runtime bugs from missing props.

#### Handling children:

```typescript
interface UserComponentProps {
        title: string;
        children: React.ReactNode;
    }
    const UserComponent: React.FC<UserComponentProps> = ({title, children}) => {
         return (
              <div>
                   <h1>{title}</h1>
                       {children}
              </div>
            );
        };
```

As you can see from the above, the `children` prop lets you pass contents between a component’s opening and closing tags represented by a large range of data types, like text, other components, or even multiple elements. This allows you to make components more flexible and reusable by letting them “wrap” or display whatever content you put inside them.

## Using discriminated unions for conditional rendering

### What are discriminated unions, and when should you use them?

When you build an app with TypeScript and React, you often deal with a single piece of data that can be in various states: loading, error, or success. Discriminated unions, sometimes called tagged unions or algebraic data types (ADTs), provide a tidy way to model these different forms. By grouping related types under one label, you keep type safety while easing the mental load during coding.

This clear separation makes it simple to decide which UI to show in your components because each state carries its own signature. In the examples that follow, we’ll see how this approach helps us write safer, more readable, and still expressive code:

```typescript
type DataLoadingState = {
  status: 'request loading...';
};

type DataSuccessState<T> = {
  status: 'request success';
  data: T;
};

type DataErrorState = {
  status: 'request error';
  message: string;
};

type DataState<T> = DataLoadingState | DataSuccessState<T> | DataErrorState;
```

From the code snippet above, each type has a common trait, usually known as a discriminator or tag, that marks its kind, much like a status label. TypeScript leans on this tag whenever the shapes are piled into a union to tell them apart. Because each shape carries a distinct fixed value for that trait, the language knows exactly which one it is and can trim the type accordingly. Once the shapes are defined, you bundle them with the `|` operator, allowing you to model complex state in a way that stays safe and predictable.

### Exhaustive checking with the never type

Exhaustive checking with the `never` type in TypeScript is a technique that ensures that all possible cases of a discriminated union are explicitly handled in a switch statement or conditional logic, allowing developers to catch unhandled scenarios at compile time through type safety.

It is worth noting that the `never` type represents a value that never occurs, i.e., unreachable code, and is used in exhaustive checks to ensure all cases of a discriminated union are properly handled. If a new case is added but not addressed, the compiler throws an error, which enhances type safety:

```typescript
function DisplayData<T>({ state }: { state: DataState<T> }) {
  switch (state.status) {
    case 'loading':
      return <p>Loading Data</p>;
    case 'success':
      return <p>Data: {JSON.stringify(state.data)}</p>;
    case 'error':
      return <p>Error: {state.message}</p>;
    default:
      return <p>Unknown status</p>;
  }
}
```

The above illustrates the final step in using discriminated unions effectively in React components by employing conditional logic like a `switch` or an `if` statement based on the discriminator property (status). This will allow you to render different UI elements depending on the current state and catch missing branches at compile time, keeping your components both type-safe and error-resistant.

---

![](https://blog.logrocket.com/wp-content/uploads/2022/11/Screen-Shot-2022-09-22-at-12.55.13-PM.png)

## [Over 200k developers use LogRocket to create better digital experiences](https://lp.logrocket.com/blg/learn-more)

---

## Inferring types from APIs with ReturnType and typeOf

Two powerful utilities by TypeScript are `typeof` and `ReturnType<T>`, which are used to infer types from existing values and extract the return type of functions, respectively, enabling safer and more maintainable code, especially when working with services, APIs, and utility functions.

### Using typeOf to infer types from functions or constants

For constants, `typeOf` is used to infer the type of a variable (string) so it’s reusable throughout without the need for hardcoding it, as shown below:

```typescript
const API_BASE_URL = "https://api.newpayment.com/services/api/v1/transfer";
type ApiBaseUrlType = typeOf API_BASE_URL;
```

You can also use `typeOf` to get the function type, which is useful for typing callbacks:

```typescript
const getEmployeeDetails = (employeeId: number) => ({
    employeeId,
    employeeName: "Peter Aideloje",
    employeeEmail: "aidelojepeter123@gmail.com",
    position: "Software Engineer",
});

// using typeof to get the function type
type GetEmployeeDetailsFnType = typeof getEmployeeDetails;
```

### Leveraging ReturnType<T> for function results

This pattern is very useful when a utility/service function returns structured data. This way, you automatically derive the result type using `Returntype`, ensuring consistency across your code base. By combining `Returntype` and `typeof`, you keep types synchronized with function signatures, avoiding manual duplication and reducing the risk of type mismatch:

```typescript
// Get the return type of the getUser function
const employeeDetails : EmployeeDetails = {
    employeeId = 3,
    employeeName: "Peter Aideloje",
    employeeEmail: "aidelojepeter123@gmail.com",
    position: "Software Engineer", 
};

type EmployeeDetails = ReturnType<typeof getEmployeeDetails>;
```

### Extracting types from services and utility functions

This helps to derive the result type automatically from the structured data of a utility or service function, thereby ensuring consistency in consuming components, as shown below:

```typescript
//utility function
function calculateTotalFee (price: number, quantity: number){
  return {
     total: price * quantity,
     currency: "GBP",
  };
}

// extracting return type of utility function
type TotalSummary = ReturnType<typeof calculateTotalFee>;

const summary: TotalSummary = {
  total: 100,
  currency: "GBP",
};
```

## Utility types: Pick, Omit, Partial, Record

TypeScript comes with a set of [built-in utility types](https://blog.logrocket.com/using-built-in-utility-types-typescript/) that make it easier to build new types from the ones you’ve already defined flexibly. These tools help to shape component props, organize state, reduce redundancy, and improve code maintainability in React projects. Below are some practical use cases of the most commonly used utility types you’ll find handy in a React + TypeScript setup.

### Practical use cases for each utility type

#### (i) Pick<Type, Keys>

The `Pick` utility type is used to construct a new type by selecting specific properties from a large `Type` thereby enhancing type safety and reducing redundancy:

```typescript
interface Employee{
          employeeId: number,
          employeeName: String,
          employeeEmail: String,
          employeePosition: String,
}
type EmployeePreview = Pick<Employee, 'employeeId' | 'employeeName'>;
const preview : Employeepreview = {
         employeeId: 35,
         employeeName: "Peter Aideloje",
};
```

This is great for displaying minimal data in a list or component.

#### (ii) Omit<Type, Keys>

The `Omit` utility type is the direct opposite of `Pick` type, used to create a new type by excluding specific properties from an existing type:

```typescript
interface Employee{
          employeeId: number,
          employeeName: String,
          employeeEmail: String,
          employeePosition: String,
}

type EmployeeWithoutEmail = Omit<Employee, 'employeeEmail'>;
const employee : EmployeeWithoutEmail = {
         employeeId: 35,
         employeeName: "Peter Aideloje",
         employeePosition: "Software Engineer",
};
```

This is great for excluding unnecessary information or sensitive fields such as passwords, email, or database ID.

#### (iii) Partial<Type>

The `Partial` utility type makes all properties in a type optional. This is useful when you are updating an object when not all properties must be provided:

```typescript
interface Employee{
          employeeId: number,
          employeeName: String,
          employeeEmail: String,
          employeePosition: String,
}

type PartialEmployee = Partial<Employee>;
const partialEmployee : PartialEmployee = {
         employeeName: "Peter Aideloje",
};
```

#### (iv) Record<Keys, Type>

The `Record` utility type creates an object with a specific set of keys and types:

```typescript
type Roles = "admin" | "employee" | "viewer";

type Permissions = Record<Role, string[]>;

const permissions: Permissions = {
     admin["read", "write", "delete"],
     employee["read", "write"],
     viewer["read"],
};
```

Utility types in TypeScript help to reduce code repetition when defining props or state by reusing and reshaping existing types. They’re also great for modelling flexible data structures, such as dynamic form inputs or API responses, making your codebase cleaner and easier to maintain.

## Generic components and hooks

### Writing reusable components with generics

Generics in TypeScript help developers to make reusable UI elements capable of managing multiple data types while keeping strong type safety. They shine better and are more important when used in React to design components that are not tied to a particular data type. This flexibility makes your React component more dynamic and can fit into various types as required in any part of your application. To achieve this, follow these steps below to set up your project:

First, open your terminal or command prompt to run the command to create a new React project using TypeScript:

```
npx create-react-app react-project --template typescript
```

Next, this command navigates you to the project directory:

```
cd react-project
```

#### Folder structure:

![Project Structure](https://blog.logrocket.com/wp-content/uploads/2025/06/project-structure.png)

Next, we’ll create a generic `List` component that can showcase a list of items of any type using the following code snippet below:

```typescript
import React from 'react';

// A Generic component
type Props<T> = {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
};

function GenericComponent<T>({ items, renderItem }: Props<T>): JSX.Element {
   return <div>{items.map(renderItem)}</div>;
}

export default GenericComponent;
```

The `GenericComponent` defines a reusable generic list component in a React + TypeScript setup. It accepts two props: an array of items and a `renderItem` function, which determines how each item should be displayed. The use of generics allows this component to work with any data type, making it a more flexible and type-safe solution for rendering lists across various use cases.

### Typing Refs and DOM elements

#### Using useRef with DOM elements

In React development, it’s necessary to leverage the built-in tools that the library provides, such as [`useRef`](https://blog.logrocket.com/react-useref/). When using `useRef` with DOM elements like `HTMLInputElement`, you need to specify the ref as shown below:

```typescript
import React, {useRef, useEffect} from 'react';
const FocusInput: React.FC = () => {
    const nameInputRef = useRef<HTMLInputElement | null>(null);
    useEffect ( () => {
       nameInputRef.current?.focus();
    }, []);
    return (
       <div>
          <label> htmlFor= "name">Name:</label>
          <input id="name" type="text" ref={nameInputRef} />
       </div>
      );
   };   

  export default FocusInput;
```

#### Forwarding refs with React.forwardRef

In React, the [`forwardRef`](https://blog.logrocket.com/use-forwardref-react/) is a handy feature that lets you pass a ref from a parent component down to a child component. This comes in useful when the child component wraps a DOM element but does not directly expose it. Essentially, `React.forwardRef` allows parent components to directly access the inner DOM node (child component’s DOM) even when it’s hidden or wrapped in other layers of abstraction. When working with TypeScript, you’ll need to define the type of the ref to keep things safe and predictable. It’s a great way to make your components more flexible and maintainable:

```typescript
import React, {forwardRef, useRef, useImperativeHandle } from 'react';

type ButtonProps = {
  handleClick?: () => void;
};

const CustomerButton = forwardRef<HTMLButtonElement, ButtonProps> ((props, ref) => { 
   const internalRef = useRef<HTMLButtonElement>(null);

   useImperativeHandle(ref, () => ({
      focus: () => {
        internalRef.current?.focus();
      },
    }));

   return (
     <button ref={internalRef} onClick={props.hanldeClick}>
      Press Here
     </button>
    );
  });

const WrapperComponent = () => {
     const refToButton = useRef<HTMLButtonElement>(null);

     const triggerFocus = () => {
         refToButton.current?.focus();
      };
   return (
     <div>
        <customButton ref={refToButton} handleClick={triggerFocus} />
     </div>
    );
 };

export default WrapperComponent;
```

#### Avoiding any DOM manipulations

In React, try your best to avoid [directly changing the DOM](https://react.dev/learn/manipulating-the-dom-with-refs) yourself. Instead, adopt a more reliable and maintainable approach to use React’s built-in state system to manage changes. For instance, rather than using a ref to manually set the value of an input field, you should let React control it through state. This keeps your component predictable and easier to debug:

```typescript
import React, {useState, useRef, useEffect } from 'react';

function ControlledInput() {
   const [inputValue, setInputValue] = useState('');
   const inputRef = useRef<HTMLInputElement>(null);

   const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
      setInputValue(event.target.value);
   };

 useEffect(() => {
 if (inputRef.current){
   //Accessing property safely
  console.log(inputRef.current.value);
  // Do not directly manipulate the DOM, use React state instead
 }
}, [inputValue]);
    return <input
                  type ="text" 
                  ref{inputRef} 
                  value{inputValue} 
                  onChange={handleInputChange} 
          />;
     }
```

## Context with strong typing

### Creating and consuming context with generic types

When you build an app with React and TypeScript, the [`createContext`](https://react.dev/reference/react/createContext) method lets you pass things like theme preferences or logged-in user details to distant components without drilling props through every layer. To keep that process type-safe and easy to manage, start by writing a TypeScript type or interface that clearly lists every piece of data the context will hold. Doing so lets the compiler flag mistakes early and keeps the shape of your context consistent wherever you import it.

After you have your type, pass a sensible default value to `React.createContext` and supply that value as the argument. The default value makes sure that any component reading the context outside of a Provider gets a safe fallback rather than crashing the app. Introduced in React 16, the [Context API](https://blog.logrocket.com/react-context-tutorial/) has become the go-to method for sharing state globally in a cleaner, more scalable fashion. Below, we’ll walk through three straightforward steps to create the context, provide it, and then consume it in a component.

#### Define the context with an interface

```typescript
interface AppContextType{
  currentValue: string;
  updateValue(updated: string) => void;
}
```

#### Create the context

```typescript
import React from 'react';

const AppContext = React.createContext<AppContextType>({
      currentValue: 'default',
      updateValue: () => {}, //Temporary function placeholder

 })
```

#### Consume the context

```typescript
import React, { useContext } from 'react';
import { AppContext } from './AppContextProvider'; //Assume context is defined in a separate file

function infoDisplay() {
     const { currentValue, updateValue} = useContext(AppContext);

return(
     <section>
            <p>Current Context: {currentValue}</p>
            <button onClick ={()=> updateValue('updateContext')}>Change Value</button>
     </section>
  );
}
```

### Using createContext with default values and undefined checks

When working with a [`createContext`](https://blog.logrocket.com/how-to-use-react-context-typescript/) in a React + TypeScript setup, care must be taken to define default values and account for cases where the context might be `undefined`. This will help you ensure that your application remains safe, predictable, and less prone to runtime errors.

#### Default value in createContext

When you call `createContext` in React, you can pass a default value as an argument. That value is what `useContext` gives back when a component reading the context isn’t inside the correct Provider, or when the Provider itself sets the value to `undefined`:

```typescript
interface IThemeContext {
  theme: 'light'|'dark';
  switchTheme: () => void;
}

const ThemeContext = React.createContext<IThemeContext | null>(null);
```

#### Handling undefined with useContext

When you pull data with the `useContext` Hook in React but forget to wrap the component in its matching Provider, or if that Provider accidentally sends `undefined`, the hook just hands you `undefined`. To keep TypeScript happy and give your app a safety net against sneaky runtime errors, always add a quick check after you read the context. That way, your component can react calmly when the context is missing instead of crashing loudly:

```typescript
import { createContext, useContext } from 'react';

interface ContextShape {
   data: string;
}

const customContext = createContext<ContextShape | undefined>(undefined);

export function useCustomContext() {
   const ctx = useContext(CustomContext);
   if (!ctx) {
      throw new Error("useCustomContext must be used within a customProvider");
    }
    return ctx;
  }

export function CustomProvider ({ children }: { children: React.ReactNode }) {
  const contextValue: contextShape = { data: "Shared context data"};
  return (
    <CustomContext.Provider value={contextValue}>
      {children}
    </CustomContext.Provider>
   );
}
```

## Conclusion

We have seen the crucial role that TypeScript plays in modern React development by helping teams to build more scalable, robust, and maintainable applications with increased code readability. Developers can use features like `typeof`, `ReturnType` to infer types from APIs, thereby reducing manual duplications and keeping types in sync with actual implementation. Additionally, when you enable typed component props and default props in your code base, you can catch misuse early and improve code readability, as shown in this article.

TypeScript also shines in handling lower-level concerns like type refs and DOM elements, bringing more clarity and safety when working with React context, which enables strong typing across consumer components.

If you’re new to these patterns, don’t feel pressured to adopt everything at once. Adopting TypeScript in React doesn’t have to be overwhelming; you can start small by incorporating it where it brings immediate value, and build it up from there. Over time, these practices will become second nature with a long-term payoff in maintainability, code quality, and making it worth the investment.

---

### More great articles from LogRocket:

- Don't miss a moment with [The Replay](https://lp.logrocket.com/subscribe-thereplay), a curated newsletter from LogRocket
- [Learn](https://blog.logrocket.com/rethinking-error-tracking-product-analytics/) how LogRocket's Galileo AI watches sessions for you and proactively surfaces the highest-impact things you should work on
- Use React's useEffect [to optimize your application's performance](https://blog.logrocket.com/understanding-react-useeffect-cleanup-function/)
- Switch between [multiple versions of Node](https://blog.logrocket.com/switching-between-node-versions-during-development/)
- [Discover](https://blog.logrocket.com/using-react-children-prop-with-typescript/) how to use the React children prop with TypeScript
- [Explore](https://blog.logrocket.com/creating-custom-mouse-cursor-css/) creating a custom mouse cursor with CSS
- Advisory boards aren’t just for executives. [Join LogRocket’s Content Advisory Board.](https://lp.logrocket.com/blg/content-advisory-board-signup) You’ll help inform the type of content we create and get access to exclusive meetups, social accreditation, and swag

---

Happy coding!

[View all posts](https://blog.logrocket.com/)

Would you be interested in joining LogRocket's developer community?

Join LogRocket’s Content Advisory Board. You’ll help inform the type of content we create and get access to exclusive meetups, social accreditation, and swag.

[Sign up now](https://lp.logrocket.com/blg/content-advisory-board-signup)