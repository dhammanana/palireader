import React from 'react';

type ContentDisplayProps = {
  content: { [key: string]: any[] };
};

export default function ContentDisplay({ content }: ContentDisplayProps) {
  return (
    <div className="pl-4">
      {Object.entries(content).map(([para, items]) => (
        Array.isArray(items) ? (
          <div key={para} className="relative bg-white p-4 rounded-lg shadow mb-4 border border-gray-200">
            <span className="absolute top-2 right-2 text-gray-500 text-sm font-semibold">#{para}</span>
            <div className="prose max-w-none">
              {items.map((item, i) => (
                <React.Fragment key={i}>
                  <div>
                    {item.sentence_content && (
                      <p className="text-red-800" dangerouslySetInnerHTML={{ __html: item.sentence_content }} />
                    )}
                    {item.translation_content && (
                      <p className="text-blue-900 mt-2" dangerouslySetInnerHTML={{ __html: item.translation_content }} />
                    )}
                    {item.translation_content_2 && (
                      <p className="text-blue-900 mt-2" dangerouslySetInnerHTML={{ __html: item.translation_content_2 }} />
                    )}
                  </div>
                  <hr />
                </React.Fragment>
              ))}
            </div>
          </div>
        ) : null
      ))}
    </div>
  );
}