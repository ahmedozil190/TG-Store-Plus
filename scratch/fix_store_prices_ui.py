import re

with open('templates/admin_store.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace the store-user-prices map block.
# Finding the block in admin_store.html
start_str = "container.innerHTML = paged.map(item => `"
end_str = "            `).join('');"

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx)

if start_idx != -1 and end_idx != -1:
    old_block = content[start_idx:end_idx + len(end_str)]
    
    new_block = """            let html = '';
            paged.forEach(up => {
                html += `
                <div class="user-card" style="position: relative; cursor: default; margin-bottom: 15px;">
                    <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 15px;">
                        <!-- Country Name -->
                        <div style="background: transparent; border: 1px solid var(--border); padding: 14px 18px; border-radius: 12px; display: flex; justify-content: space-between; align-items: flex-start; gap: 20px;">
                            <span style="color: var(--text-secondary); font-size: 0.8rem; font-weight: 700; text-transform: uppercase; flex-shrink: 0;">${currentLang === 'ar' ? 'الدولة' : 'Name'}</span>
                            <span style="color: var(--success); font-weight: 800; font-size: 1.1rem; text-align: right; word-break: break-all; flex: 1; min-width: 0;">${up.country_name}</span>
                        </div>
                        <!-- Country Code -->
                        <div style="background: transparent; border: 1px solid var(--border); padding: 14px 18px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: var(--text-secondary); font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">${currentLang === 'ar' ? 'كود' : 'Code'}</span>
                            <span style="color: var(--accent-purple); font-weight: 800; font-size: 1.1rem;">+${up.country_code}</span>
                        </div>
                        <!-- Sell Price -->
                        <div style="background: transparent; border: 1px solid var(--border); padding: 14px 18px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: var(--text-secondary); font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">${currentLang === 'ar' ? 'السعر' : 'Price'}</span>
                            <span style="color: var(--accent); font-weight: 900; font-size: 1.1rem;">$${Number(up.sell_price).toFixed(2)}</span>
                        </div>
                        <!-- User Name -->
                        <div style="background: transparent; border: 1px solid var(--border); padding: 14px 18px; border-radius: 12px; display: flex; justify-content: space-between; align-items: flex-start; gap: 20px;">
                            <span style="color: var(--text-secondary); font-size: 0.8rem; font-weight: 700; text-transform: uppercase; flex-shrink: 0;">${currentLang === 'ar' ? 'المستخدم' : 'User'}</span>
                            <span style="color: #3b82f6; font-weight: 800; font-size: 0.95rem; text-align: right; word-break: break-all; flex: 1; min-width: 0;">${up.user_name}</span>
                        </div>
                        <!-- User ID -->
                        <div style="background: transparent; border: 1px solid var(--border); padding: 14px 18px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: var(--text-secondary); font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">${currentLang === 'ar' ? 'معرف المستخدم' : 'User ID'}</span>
                            <span style="color: #f59e0b; font-weight: 800; font-size: 1.1rem;"><code>${up.user_id}</code></span>
                        </div>
                    </div>
                    <!-- Action Buttons -->
                    <div style="display: flex; gap: 10px;">
                        <button class="primary-btn" style="flex: 1; background: rgba(96, 165, 250, 0.1); color: var(--accent); border: 1px solid rgba(96, 165, 250, 0.2); box-shadow: none; padding: 14px; font-size: 0.95rem;" onclick='editStoreUserPrice(${JSON.stringify(up).replace(/'/g, "&#39;")})'>
                            <i class="fas fa-edit" style="${currentLang === 'ar' ? 'margin-left: 8px;' : 'margin-right: 8px;'}"></i> ${currentLang === 'ar' ? 'تعديل' : 'Edit'}
                        </button>
                        <button class="primary-btn" style="flex: 1; background: rgba(239, 68, 68, 0.1); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.2); box-shadow: none; padding: 14px; font-size: 0.95rem;" onclick="deleteStoreUserPrice(${up.id})">
                            <i class="fas fa-trash" style="${currentLang === 'ar' ? 'margin-left: 8px;' : 'margin-right: 8px;'}"></i> ${currentLang === 'ar' ? 'حذف' : 'Delete'}
                        </button>
                    </div>
                </div>`;
            });
            container.innerHTML = html;"""
            
    content = content.replace(old_block, new_block)
    
    with open('templates/admin_store.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced successfully.")
else:
    print("Target block not found.")
