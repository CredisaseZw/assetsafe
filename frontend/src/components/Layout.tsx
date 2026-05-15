import React from 'react';
import { Link } from 'react-router-dom';

export const LeftNav: React.FC = () => {
  return (
    <aside className="left-nav" aria-label="Primary navigation">
      <div className="nav-brand">AssetSafe</div>
      <nav>
        <Link to="/">Dashboard</Link>
        <Link to="/assets">Assets</Link>
        <Link to="/collateral">Collateral</Link>
        <Link to="/companies">Companies</Link>
        <Link to="/users">Users</Link>
      </nav>
    </aside>
  );
};

const Layout: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  return (
    <div className="app-layout">
      <LeftNav />
      <main className="main-content">{children}</main>
    </div>
  );
};

export default Layout;
