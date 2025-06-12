import React, { useState } from 'react';
import { Layout, Button } from 'antd';
import Sidebar from './Sidebar.jsx';
import TranslationViewer from './TranslationViewer.jsx';

const { Header, Sider, Content } = Layout;

const App = () => {
    const [collapsed, setCollapsed] = useState(true);

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Header style={{ background: '#001529', padding: '0 16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ color: '#fff', fontSize: '18px' }}>Nissaya Translation Viewer</span>
                    <Button
                        type="text"
                        icon={<i className="bi bi-list" />}
                        onClick={() => setCollapsed(!collapsed)}
                        style={{ color: '#fff' }}
                    />
                </div>
            </Header>
            <Layout>
                <Sider
                    collapsible
                    collapsed={collapsed}
                    onCollapse={setCollapsed}
                    trigger={null}
                    style={{ background: '#fff' }}
                    width={250}
                >
                    <Sidebar />
                </Sider>
                <Content style={{ padding: '16px', marginLeft: collapsed ? 80 : 250, transition: 'margin-left 0.2s' }}>
                    <TranslationViewer />
                </Content>
            </Layout>
        </Layout>
    );
};

export default App;
